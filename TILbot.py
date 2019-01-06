import requests

class Post:

    def __init__(self, timeStamp, postId, title, sourceUrl):
        self.timeStamp = timeStamp
        self.postId = postId
        self.title = title
        self.sourceUrl = sourceUrl

def get_data():
    url = "https://www.reddit.com/r/todayilearned/new/.json"

    try:
        data = requests.get(url, headers={'User-agent': 'beginner-project-jirc'})
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
        title = post['data']['title']
        sourceUrl = post['data']['url']
        postId = post['data']['id']

        posts.append(Post(timeStamp, postId, title, sourceUrl))

    return posts


for post in get_new_posts():
    print(post.timeStamp)