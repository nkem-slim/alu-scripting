#!/usr/bin/python3
"""Module for top_ten function"""
import requests


def top_ten(subreddit):
    """Query the Reddit API and print the titles of the top 10 posts."""
    url = "https://www.reddit.com/r/{}/hot.json?limit=10".format(subreddit)
    headers = {'User-Agent': 'My User Agent 1.0'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json().get('data').get('children')
        for post in data:
            print(post.get('data').get('title'))
    else:
        print(None)


subreddit_name = "learnpython"  
top_ten(subreddit_name)
