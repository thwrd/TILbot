import requests
import html

class Post:

    def __init__(self, timeStamp, postId, title, permaLink, sourceUrl):
        self.timeStamp = timeStamp
        self.postId = postId
        self.title = title
        self.permaLink = f'https://reddit.com{permaLink}'
        self.sourceUrl = sourceUrl

    def is_new(self, dbConnection):
        cur = dbConnection.cursor()
        cur.execute('''SELECT timeStamp FROM facts ORDER BY timestamp DESC LIMIT 1 ;''')
        newestTimeStamp = cur.fetchone()
        if newestTimeStamp is None or newestTimeStamp[0] < self.timeStamp:
            return True
        else:
            return False

    def save_post(self, dbConnection):
        sql = '''
              INSERT INTO facts (timeStamp, postId, title, permaLink, sourceUrl)
              VALUES (:timeStamp, :postId, :title, :permaLink, :sourceUrl)
              '''
        with dbConnection:
            cur = dbConnection.cursor()
            cur.execute(sql, {'timeStamp': self.timeStamp, 'postId': self.postId, 'title': self.title,
                              'permaLink': self.permaLink, 'sourceUrl': self.sourceUrl})


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
        title = html.unescape(post['data']['title']).lstrip('TIL -:').capitalize()
        sourceUrl = post['data']['url']
        postId = post['data']['id']
        permaLink = post['data']['permalink']

        posts.append(Post(timeStamp, postId, title, permaLink, sourceUrl))
    # sort list oldest to newest
    return sorted(posts, key=lambda x: x.timeStamp)