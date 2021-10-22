import requests
import json
import time
from datetime import datetime


f = open("./credentials.json", "r")
credentials = json.load(f)

CLIENT_ID = credentials["CLIENT_ID"]
OAUTH_TOKEN = credentials["OAUTH_TOKEN"]

f.close()

streamers = ["xqcow", "hasanabi", "ludwig", "nl_kripp", "lirik", "shroud", "mizkif", "gmhikaru"]

def is_user_live(username):
    endpoint = 'https://api.twitch.tv/helix/streams?'
    my_headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {OAUTH_TOKEN}'
    }
    my_params = {'user_login': username}
    response = requests.get(endpoint, headers=my_headers, params=my_params)
    data = response.json()['data']
    if len(data) == 0:
        return False

    return data[0]['type'] == 'live'

def get_viewers(name):
    url = f"http://tmi.twitch.tv/group/user/{name.lower()}/chatters"
    response = requests.get(url)
    response = response.json()

    viewers = set(response['chatters']['viewers'])
    
    return viewers

def update_data(streamer):
    with f as open(streamer+".csv", "a"):
        pass

def main():

    while True:
        for streamer in streamers:
            if is_user_live(streamer):
                update_data(streamer)
        
        time.sleep(5)

if __name__ == '__main__':
    main()
