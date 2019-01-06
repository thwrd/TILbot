import requests
import json
import yaml
from time import sleep
from reddit_functions import get_new_posts

with open('config.yaml', 'r') as f:
    conf = yaml.load(f)

slackHook = conf['slackHook']
mostRecentPost = conf['mostRecentTimestamp']

headers={'Content-type':'application/json'}

def format_slack_post(message, source, comments):
    slackPost = {'text': f'_*Fresh fact, hot off the press!*_\n>{message}\n>*Read more:* `{source}`\n>*Join the conversation:* `{comments}`'}
    return json.dumps(slackPost)

while True:
    for post in get_new_posts():
        if post.timeStamp > mostRecentPost:
            slackPost = format_slack_post(post.title, post.sourceUrl, post.permaLink)
            # requests.post(slackHook, data = slackPost, headers = headers)
            print(slackPost)
            mostRecentPost = post.timeStamp
            conf['mostRecentTimestamp'] = mostRecentPost
            with open('config.yaml', 'w') as f:
                yaml.dump(conf, f)

    sleep(60)