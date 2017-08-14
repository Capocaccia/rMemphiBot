# A reddit bot that responds to FAQ in the /r/Memphis subreddit.
# Created by /u/CaptainInsane-o
# License: MIT License

from bs4 import BeautifulSoup
from urllib.parse import urlparse

import praw
import time
import re
import requests
import bs4

path = '/Users/Carter/code/rMemphiBot/commented.txt'
# Location of file where id's of already visited comments are maintained

header = 'Header Here'
footer = 'Footer Here'
# Text to be posted along with comic description


def authenticate():

    print('Authenticating...\n')
    reddit = praw.Reddit('MemBot', user_agent = 'web:A FAQ bot for /r/Memphis (by /u/CaptainInsane-o)')
    print('Authenticated as {}\n'.format(reddit.user.me()))
    return reddit


def fetchdata(url):

    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    tag = soup.find('p')
    data = ''
    while True:
        if isinstance(tag, bs4.element.Tag):
            if (tag.name == 'h2'):
                break
            if (tag.name == 'h3'):
                tag = tag.nextSibling
            else:
                data = data + '\n' + tag.text
                tag = tag.nextSibling
        else:
            tag = tag.nextSibling

    return data


def run_membot(reddit):

    print("Getting 250 posts...\n")

    for post in reddit.subreddit('test').new(limit = 250):
        match = re.findall("\W*(barbecue)\W*", post.title)
        if match:
            print('Matched!')
            file_obj_r = open(path,'r')

            try:
                explanation = 'BARBECUE INFO'
            except:
                print('Exception!!! Possibly incorrect xkcd URL...\n')
                # Typical cause for this will be a URL for an xkcd that does not exist (Example: https://www.xkcd.com/772524318/)
            else:
                if post.id not in file_obj_r.read().splitlines():
                    print('Link is unique...posting explanation\n')
                    post.reply(header + explanation + footer)

                    file_obj_r.close()

                    file_obj_w = open(path,'a+')
                    file_obj_w.write(post.id + '\n')
                    file_obj_w.close()
                else:
                    print('Already visited link...no reply needed\n')

            time.sleep(10)

    print('Waiting 60 seconds...\n')
    time.sleep(60)


def main():
    reddit = authenticate()
    while True:
        run_membot(reddit)


if __name__ == '__main__':
    main()
