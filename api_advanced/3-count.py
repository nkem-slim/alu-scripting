#!/usr/bin/python3
""" 3-count.py """
import json
import requests

def count_words(subreddit, word_list, after=None, count={}):
    """Prints a sorted count of given keywords in hot posts of a subreddit."""

    if after is None:
        after = ""

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {'User-Agent': 'Mozilla/5.0'}
    params = {'after': after, 'limit': 100}  # Limit to 100 posts per request

    response = requests.get(url, params=params, headers=headers, allow_redirects=False)

    if response.status_code != 200:
        print("Request failed with status code:", response.status_code)
        return

    data = response.json()

    if count == {}:
        count = {word.lower(): 0 for word in word_list}

    for post in data['data']['children']:
        title = post['data']['title'].lower()
        for word in word_list:
            count[word] += title.count(word)

    after = data['data']['after']

    if after:
        count_words(subreddit, word_list, after, count)
    else:
        sorted_count = sorted(count.items(), key=lambda x: (-x[1], x[0]))
        for word, word_count in sorted_count:
            if word_count > 0:
                print("{}: {}".format(word, word_count))

if __name__ == '__main__':
    subreddit = "unpopular"  # Change this to your desired subreddit
    keywords = ['you', 'unpopular', 'vote', 'down', 'downvote', 'her', 'politics']
    count_words(subreddit, keywords)

