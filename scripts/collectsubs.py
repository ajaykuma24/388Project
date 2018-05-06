import praw, json, sys
from pprint import pprint

print('starting')
reddit = praw.Reddit(client_id=sys.argv[1],
                     client_secret=sys.argv[2],
                     user_agent='Python:388finalproject (by /u/LostWillingness)')
sub = sys.argv[3].lower()
print(sub)

usernames = set()
user_subs = dict()

with open('users/' + sub + '.json') as f:
    usernames = set(json.load(f))

for user in usernames:
    user_subs[user] = {sub,}

print(len(usernames))
users = list(reddit.redditor(name) for name in usernames)

user_errs = 0
with open('subs/' + sub + '.json', 'w') as f:
    for user in users:
        try:
            for comment in user.comments.top('month'): # search 100 top comments
                subs = user_subs[user.name]
                subs.add(str(comment.subreddit).lower())
                user_subs[user.name] = subs
        except:
            user_errs += 1
    for user in user_subs:
        user_subs[user] = list(user_subs[user])
    json.dump(user_subs, f, separators=(',', ':'))

print('errors ' + str(user_errs))
print(len(user_subs.keys()))
print('done')

