import requests
import json
import pandas as pd
# note that CLIENT_ID is 'personal use script' and SECRET_TOKEN to 'token'
auth = requests.auth.HTTPBasicAuth('jXmLv7BeBIYBeg', 'K6AT6c8ccwisKUOqgPFn-PekBuQmXQ')

# here we pass our login method (password), username, and password
data = {'grant_type': 'password',
        'username': 'hipstervkitty',
        'password': 'O2zL6gb0gUARkxvkJ0Gd'}

# setup our header info, which gives reddit a brief description of our app
headers = {'User-Agent': 'MyBot/0.0.1'}

# send our request for an OAuth token
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

# convert response to JSON and pull access_token value
TOKEN = res.json()['access_token']

# add authorization to our headers dictionary
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

# while the token is valid (~2 hours) we just add headers=headers to our requests
requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)


res = requests.get("https://oauth.reddit.com/user/HiPSTERvKiTTY/saved/",
                   headers=headers)

linkDF = pd.DataFrame()  # initialize dataframe
commentDF = pd.DataFrame() 
#print(res.json())  
for post in res.json()['data']['children']:
       
        if post['kind'] == 't3':
           linkDF = linkDF.append({
                'subreddit': post['data']['subreddit'],
                'title': post['data']['title'],
                'selftext': post['data']['selftext'],
                'upvote_ratio': post['data']['upvote_ratio'],
                'ups': post['data']['ups'],
                'url': post['data']['permalink'],
                'author': post['data']['author']
            }, ignore_index=True)

        elif post['kind'] == 't1':
            commentDF = commentDF.append({
                'subreddit': post['data']['subreddit'],
                'body': post['data']['body_html'],
                'ups': post['data']['ups'],
                'url': post['data']['link_url'],
                'author': post['data']['author']
            }, ignore_index=True)
                

