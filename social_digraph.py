import networkx as nx
import pandas as pd
import json
from datetime import datetime
from entity_graph_creator import draw_graph, save_graph_files


def create_graph(users):
    graph = nx.DiGraph()

    for user in users:
        print(user)
        f = open('jsons/' + user + '_followers.json')
        json_object = json.load(f)

        graph.add_node(user, data='')

        for follower in json_object:
            screen_name = follower['screen_name']
            date_obj = datetime.strptime(follower['created_at'], "%a %b %d %X %z %Y")

            graph.add_node(screen_name, data=date_obj.strftime('%Y-%m-%d'))
            graph.add_edges_from([(screen_name, user)], weight=1)

        f.close()

        f = open('jsons/' + user + '_following.json')
        json_object = json.load(f)

        for following in json_object:
            screen_name = following['screen_name']
            date_obj = datetime.strptime(following['created_at'], "%a %b %d %X %z %Y")
            data_str = date_obj.strftime('%Y-%m-%d')
            graph.add_node(screen_name, data=data_str)
            graph.add_edges_from([(user, screen_name)], weight=1)

        f.close()

    return graph


if __name__ == '__main__':
    names = ['LIST','OF','SCREEN_NAMES']
    graph = create_graph(names)
    save_graph_files(graph, 'filename.gexf')

