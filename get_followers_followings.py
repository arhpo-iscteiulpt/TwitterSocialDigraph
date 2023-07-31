import requests
import os
import json
import time

os.environ['TOKEN'] = 'YOUR TWITTER API ACCESS TOKEN'

def auth():
    return os.getenv('TOKEN')


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def create_url_followers(screen_name, count):
    search_url = "https://api.twitter.com/1.1/followers/list.json"

    # change params based on the endpoint you are using
    query_params = {'screen_name': screen_name,
                    'count': count,
                    'cursor': {}}
    return search_url, query_params


def create_url_following(screen_name, count):
    search_url = "https://api.twitter.com/1.1/friends/list.json"

    # change params based on the endpoint you are using
    query_params = {'screen_name': screen_name,
                    'count': count,
                    'cursor': {}}
    return search_url, query_params


def connect_to_endpoint(url, headers, params, next_cursor):
    params['cursor'] = next_cursor  # params object received from create_url function
    print(params)
    response = requests.request("GET", url, headers=headers, params=params)
    # print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def get_all_followers(user, count, next_cursor=-1):
    bearer_token = auth()
    headers = create_headers(bearer_token)

    url = create_url_followers(user, count)

    try:
        json_response = connect_to_endpoint(url[0], headers, url[1], next_cursor)
        followers = json_response['users']

        while next_cursor != 0:
            json_response = connect_to_endpoint(url[0], headers, url[1], next_cursor)
            followers.extend(json_response['users'])
            next_cursor = json_response['next_cursor']
            print(next_cursor)
            time.sleep(5)
    except:
        print("time limit")
        print("next_cursor ")
        print(next_cursor)

    return followers


def get_all_friends(user, count):
    bearer_token = auth()
    headers = create_headers(bearer_token)

    url = create_url_following(user, count)
    next_cursor = -1

    try:
        json_response = connect_to_endpoint(url[0], headers, url[1], next_cursor)
        following = json_response['users']

        while next_cursor != 0:
            json_response = connect_to_endpoint(url[0], headers, url[1], next_cursor)
            following.extend(json_response['users'])
            next_cursor = json_response['next_cursor']
            print(next_cursor)
            time.sleep(5)
    except:
        print("time limit")

    return following


if __name__ == '__main__':
    names = ['LIST','OF','SCREEN_NAMES']
    for name in names:
        print(name)
        list_followers = get_all_followers(name, 200)
        with open('jsons/' + name + '_followers.json', 'a') as json_file:
            json.dump(list_followers, json_file)

    for name in names:
        print(name)
        list_followers = get_all_friends(name, 200)
        with open('jsons/' + name + '_following.json', 'a') as json_file:
            json.dump(list_followers, json_file)

