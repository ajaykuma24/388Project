import praw, json, sys
from pprint import pprint

reddit = praw.Reddit(client_id=sys.argv[1],
                     client_secret=sys.argv[2],
                     user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                     (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36')
sub = sys.argv[3].lower()
print(sub)

users = set()
usernames = set()
user_subs = dict()

with open('users/' + sub + '.json', 'w') as f:
    subreddit = reddit.subreddit(sub)
    for post in subreddit.top('month'): # search 100 top posts
        post.comments.replace_more(limit=None) # all comments on each post
        comments = post.comments.list()
        for comment in comments:
            if comment.author != None:
                users.add(comment.author)
                usernames.add(comment.author.name)
                subs = user_subs.get(comment.author.name, set())
                subs.add(sub)
                user_subs[comment.author.name] = subs

    json.dump(list(usernames), f, separators=(',', ':'))

print(len(usernames))
with open('subs/' + sub + '.json', 'w') as f:
    for user in list(users):
        try:
            for comment in user.comments.top('month'): # search 100 top comments
                subs = user_subs[user.name]
                subs.add(str(comment.subreddit).lower())
                user_subs[user.name] = subs
        except:
            pass
    for user in user_subs:
        user_subs[user] = list(user_subs[user])
    json.dump(user_subs, f, separators=(',', ':'))
print("done")

