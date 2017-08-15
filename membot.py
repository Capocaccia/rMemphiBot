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

header = 'MemBot provides information about the city of Memphis Tennessee to /r/Memphis users.'
footer = 'MemBot is provided by /u/CaptainInsane-o.  Source code available upon request.'


def authenticate():

    print('Authenticating...\n')
    reddit = praw.Reddit('MemBot', user_agent = 'web:A FAQ bot for /r/Memphis (by /u/CaptainInsane-o)')
    print('Authenticated as {}\n'.format(reddit.user.me()))
    return reddit

def run_membot(reddit):

    print("Getting 250 posts...\n")

    for post in reddit.subreddit('test').new(limit = 250):
        match = re.findall("\W*(barbecue)\W*", post.title)
        if match:
            print('Matched!')
            file_obj_r = open(path,'r')

            try:
                reply = '**BBQ**' + '\n\n' + '[Tops Bar-B-Q](https://www.yelp.com/biz/tops-bar-b-q-memphis-12) - Ask for white chop, good burgers' + '\n\n' + '[Central BBQ](https://www.yelp.com/biz/central-bbq-memphis-3) – 3 locations, downtown, summer ave and midtown. Nachos with house chips' + '\n\n' + ' [Payne’s Bar-B-Que](https://www.yelp.com/biz/paynes-bar-b-que-memphis) – Slaw Dog, BBQ Baloney, CASH ONLY' + '\n\n' + '[The Bar-B-Q Shop](https://www.yelp.com/biz/the-bar-b-q-shop-memphis-5) – BBQ Spagetti' + '\n\n' + '[Corky’s Ribs & BBQ](https://www.yelp.com/biz/corkys-ribs-and-bbq-memphis-2) – Ribs and Catfish' + '\n\n' + '[Cozy Corner Restaurant](https://www.yelp.com/biz/cozy-corner-restaurant-memphis-20) – Cornish hen and rib tips' + '\n\n' + '[Commissary BBQ](http://www.commissarybbq.com) – Germantown' + '\n\n' + '[Leonard’s Pit Barbecue](https://www.yelp.com/biz/leonards-pit-barbecue-memphis) - buffet' + '\n\n' + '[Interstate Barbecue](https://www.yelp.com/biz/interstate-barbecue-memphis) – BBQ spaghetti' + '\n\n' + '[One & Only BBQ](https://www.yelp.com/biz/one-and-only-bbq-memphis-4)' + '\n\n' + '[Tom’s Barbecue and Deli](https://www.yelp.com/biz/toms-barbecue-and-deli-memphis-3) – rib tips Featured on Diners Drive Ins and Dives' + '\n\n' + '[Rendezvous BBQ](https://www.yelp.com/biz/charlie-vergos-rendezvous-memphis) – they don’t slow smoke their ribs, they grill them'
            except:
                print('Error above line 41.\n')
            else:
                if post.id not in file_obj_r.read().splitlines():
                    print('Link is unique...posting reply\n')
                    post.reply(header + '\n\n' + reply + '\n\n' + footer)

                    file_obj_r.close()

                    file_obj_w = open(path,'a+')
                    file_obj_w.write(post.id + '\n')
                    file_obj_w.close()
                else:
                    print('Already visited link...no reply will be posted\n')

            time.sleep(10)

    print('Waiting 60 seconds...\n')
    time.sleep(60)


def main():
    reddit = authenticate()
    while True:
        run_membot(reddit)


if __name__ == '__main__':
    main()


