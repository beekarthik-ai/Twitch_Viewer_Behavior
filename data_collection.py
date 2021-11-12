import requests
import csv
import json
import time
from datetime import datetime


f = open("./credentials.json", "r")
credentials = json.load(f)

CLIENT_ID = credentials["CLIENT_ID"]
OAUTH_TOKEN = credentials["OAUTH_TOKEN"]

f.close()

streamers = open("data/channels.txt").readlines()
streamers = [name[:-1] for name in streamers]

def curr_info(username):
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
    
    return data[0]

def is_user_live(curr_info_json):
    return curr_info_json

def get_viewers(name):
    url = f"http://tmi.twitch.tv/group/user/{name.lower()}/chatters"
    response = requests.get(url)
    response = response.json()

    viewers = set(response['chatters']['viewers'])
    
    return viewers

def update_data(streamer, curr_info_json):
    with open("data/all_streamer_data.csv", "a") as database:
        writer = csv.writer(database)
        #viewers = get_viewers(streamer)
        writer.writerow([streamer, datetime.now(), curr_info_json['started_at'], curr_info_json['game_name'],
                            curr_info_json['language'], curr_info_json['viewer_count'],  curr_info_json['is_mature']])

def main():
    print(streamers)
    while True:
        for streamer in streamers:
            try:
                curr_info_json = curr_info(streamer)
                if is_user_live(curr_info_json):
                    update_data(streamer, curr_info_json)
            except Exception:
                pass
            time.sleep(10)
           

if __name__ == '__main__':
    main()
