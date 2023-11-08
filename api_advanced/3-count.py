#!/usr/bin/python3
""" 3-count.py """
import json
import requests

def count_words(subreddit, word_list, after=None, counts=None):
    if counts is None:
        counts = {}  # Initialize the counts dictionary

    # Base case: if word_list is empty, we're done
    if not word_list:
        sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
        for word, count in sorted_counts:
            print(f"{word.lower()}: {count}")
        return

    if after is None:
        params = {'limit': 100}
    else:
        params = {'limit': 100, 'after': after}

    response = requests.get(f'https://www.reddit.com/r/{subreddit}/hot.json', headers={'User-agent': 'Mozilla/5.0'}, params=params)

    if response.status_code != 200:
        return  # Invalid subreddit or other issue

    data = response.json().get('data', {})
    children = data.get('children', [])

    for post in children:
        title = post['data']['title']
        for word in word_list:
            # Remove punctuation and convert to lowercase for accurate counting
            clean_title = title.lower().replace('.', ' ').replace('!', ' ').replace('_', ' ')
            word_list_copy = list(word_list)  # Create a copy to avoid modifying the original list
            if word in clean_title.split():
                counts[word] = counts.get(word, 0) + 1
                word_list_copy.remove(word)  # Remove the counted word from the list

        if not word_list_copy:  # All keywords found, continue with the next word
            continue

    if data.get('after'):
        count_words(subreddit, word_list_copy, after=data['after'], counts=counts)

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 3:
        print("Usage: {} <subreddit> <list of keywords>".format(sys.argv[0]))
        print("Ex: {} programming 'python java javascript'".format(sys.argv[0]))
    else:
        count_words(sys.argv[1], [x for x in sys.argv[2].split()])

