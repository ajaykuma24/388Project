import praw, json, sys
from pprint import pprint

client_id='GU3_zhD3Si1x-Q'
secret='aloijMaL1Ya5Y0pgbvbZ3Uu3GsA'
reddit = praw.Reddit(client_id=client_id,
                     client_secret=secret,
                     user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                     (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36')
sub = sys.argv[1].lower()
print(sub)

users = set()
usernames = set()
user_subs = dict()

with open('users/' + sub + '.json', 'w') as f:
    subreddit = reddit.subreddit(sub)
    for post in subreddit.top('month', limit=10): # search 100 top posts
        post.comments.replace_more(limit=None) # all comments on each post
        comments = post.comments.list()
        for comment in comments:
            if comment.author != None:
                users.add(comment.author)
                usernames.add(comment.author.name)
                subs = user_subs.get(comment.author.name, set())
                user_subs[comment.author.name] = subs

    json.dump(list(usernames), f, separators=(',', ':'))

print(len(usernames))
errors = 0
with open('subs/' + sub + '.json', 'w') as f:
    for user in list(users):
        try:
            for comment in user.comments.top('month'): # search 100 top comments
                subs = user_subs[user.name]
                subs.add(str(comment.subreddit).lower())
                user_subs[user.name] = subs
        except:
            pass
        errors += 1
    for user in user_subs:
        user_subs[user] = list(user_subs[user])
    json.dump(user_subs, f, separators=(',', ':'))
print(errors, 'errors')
print("done")

