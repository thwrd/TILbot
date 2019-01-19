import requests
import json
import yaml
from time import sleep
from reddit_utils import get_new_posts
from db_utils import *

# import configuration
with open('config.yaml', 'r') as f:
    conf = yaml.load(f)

# instantiate database connection and cursor
con = get_database_connection()
cur = con.cursor()

# create database tables if they don't exist
cur.execute('''SELECT 1 FROM sqlite_master WHERE type='table' AND name='facts';''')
if cur.fetchone() is None:
    create_facts_table(con)

# set request headers and slack token
slackHook = conf['slackHook']
headers={'Content-type':'application/json'}

def format_slack_post(message, source, comments):
    slackPost = {'text': f'_*Fresh fact, hot off the press!*_\n>{message}\n>*Read more:* `{source}`\n>*Join the conversation:* `{comments}`'}
    return json.dumps(slackPost)

while True:
    for post in get_new_posts():
        if post.is_new(con):
            post.save_post(con)
            slackPost = format_slack_post(post.title, post.sourceUrl, post.permaLink)
            requests.post(slackHook, data = slackPost, headers = headers)
    sleep(60)

