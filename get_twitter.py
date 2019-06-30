import json
from twython import Twython
from collections import OrderedDict

import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from time import sleep

with open('identity.json') as token_file:
    identity = json.load(token_file)
    APP_KEY = identity['APP_KEY']
    APP_SECRET = identity['APP_SECRET']
    OAUTH_TOKEN = identity['OAUTH_TOKEN']
    OAUTH_TOKEN_SECRET = identity['OAUTH_TOKEN_SECRET']

# with open('colors.csv','w') as color_file:
#     for color in mcolors.XKCD_COLORS:
#         color_file.write(color+"\n")
#         print(mcolors.to_rgba(color))
user_reqested_color_dict = OrderedDict()
OFFICIAL_COLORS = {color[5:] for color in mcolors.XKCD_COLORS}

def set_color(color_name):
    for color in OFFICIAL_COLORS:
        if color in color_name:
            print("color_name " + color_name)
            #actually set the RGBW color on the leds

def use_ml_color():
    print("using ML color")
    # put model in
    # define colors/fades

twitter = Twython(APP_KEY, APP_SECRET,
                    OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
since_id = 0
while True:
    print("starting")
    if user_reqested_color_dict:
        k, v = user_reqested_color_dict.popitem(last=False)
        set_color(v)
    else:
        use_ml_color()
    process_list = list(user_reqested_color_dict.keys())
    if len(process_list) > 0:
        since_id = process_list[-1]
    print("since_id " + str(since_id))
    results = []
    if since_id == 0:
        results = twitter.get_mentions_timeline()
        results.reverse()
    else:
        results = twitter.get_mentions_timeline(since_id = since_id)
        
    for result in results:
        if result['id'] not in user_reqested_color_dict.keys():
            user_reqested_color_dict[result['id']] = result['text']
            print(result['user']['screen_name'] + " " + result['text'])
    print("sleeping so as not to get throttled")
    sleep(13)
