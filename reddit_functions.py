import requests
import html

class Post:

    def __init__(self, timeStamp, postId, title, permaLink, sourceUrl):
        self.timeStamp = timeStamp
        self.postId = postId
        self.title = title
        self.permaLink = f'https://reddit.com{permaLink}'
        self.sourceUrl = sourceUrl

def get_data():
    url = "https://www.reddit.com/r/todayilearned/new/.json"

    try:
        data = requests.get(url, headers={'User-agent': 'TILbot-simple-py-proj'})
    except Exception as e:
        print(e)
        return -1
    else:
        return data.json()

def get_new_posts():

    posts = []
    data = get_data()

    for post in data['data']['children']:
        timeStamp = post['data']['created_utc']    
        title = html.unescape(post['data']['title']).lstrip('TIL ').capitalize()
        sourceUrl = post['data']['url']
        postId = post['data']['id']
        permaLink = post['data']['permalink']

        posts.append(Post(timeStamp, postId, title, permaLink, sourceUrl))
    # sort list oldest to newest
    return sorted(posts, key=lambda x: x.timeStamp)