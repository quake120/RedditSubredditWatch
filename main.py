import praw
import os
import re
import ast

subList = {}

reddit = praw.Reddit(client_id=os.environ['client_id'],
                     client_secret=os.environ['client_secret'],
                     user_agent="CommentAnalyticsBot v1.0")

with open('subredditList', 'r') as f:
    subList = ast.literal_eval(f.read())

for comment in reddit.subreddit('all').stream.comments():
    foundSubs = re.findall('/r/[A-Za-z0-9]+', comment.body)

    for sub in foundSubs:
        subLowerCase = sub.lower()
        if len(subList) == 0:
            print("[*] " + subLowerCase)
            subList.update({
                subLowerCase: 1,
                "originSub": comment.subreddit.name
            })

        if subLowerCase not in subList.keys():
            print("[+] " + subLowerCase)
            subList.update({
                subLowerCase: 1,
                "originSub": comment.subreddit.name
            })
        else:
            currentCount = subList[subLowerCase]
            print("[#] " + subLowerCase + " x" + str(currentCount + 1))
            newCount = currentCount + 1
            subList.update({subLowerCase: newCount})

    if len(subList) % 10 == 0:
        with open('subredditList', 'w') as f:
            f.write(str(subList))
