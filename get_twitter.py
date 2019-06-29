import json
from twython import Twython
from twython import TwythonStreamer
import queue
from time import sleep

with open('identity.json') as token_file:
    identity = json.load(token_file)
    APP_KEY = identity['APP_KEY']
    APP_SECRET = identity['APP_SECRET']
    OAUTH_TOKEN = identity['OAUTH_TOKEN']
    OAUTH_TOKEN_SECRET = identity['OAUTH_TOKEN_SECRET']


color_q = queue.Queue()
class MyStreamer(TwythonStreamer):

    def on_success(self, data):
        self.disconnect()
        for color in ['red', 'blue', 'purple', 'green', 'yellow']:
            if(color in data['text']):
                print("found " + color)
                color_q.put(color)
                print(color_q.qsize())
        return

    def on_error(self, status_code, data):
        print(status_code)
        sleep(1)

    def set_color(self, color_name):
        print("color_name " + color_name)
        #actually set the RGBW color on the leds
        return

twitter = Twython(APP_KEY, APP_SECRET,
                    OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
while True:
    print("starting")
    results = twitter.get_mentions_timeline(since_id = 1000000000000)
    for result in results:
        print(result['user']['screen_name'] + " " + result['text'])
    print("sleeping so not to get rate-limited")
    sleep(13)
