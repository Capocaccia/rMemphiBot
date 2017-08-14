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

header = 'MemBot provides information about the city of Memphis Tennessee to /r/Memphis users. /n'
footer = '/n MemBotpytho is provided by /u/CaptainInsane-o.  Source code available upon request.'
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
                explanation = '<p><strong>BBQ</strong></p><p><a href="https://www.yelp.com/biz/tops-bar-b-q-memphis-12">Tops Bar-B-Q</a> - Ask for white chop, good burgers  </p><p><a href="https://www.yelp.com/biz/central-bbq-memphis-3">Central BBQ</a> – 3 locations, downtown, summer ave and midtown. Nachos with house chips  </p><p><a href="https://www.yelp.com/biz/paynes-bar-b-que-memphis">Payne’s Bar-B-Que</a> – Slaw Dog, BBQ Baloney, CASH ONLY</p><p><a href="https://www.yelp.com/biz/the-bar-b-q-shop-memphis-5">The Bar-B-Q Shop</a> – BBQ Spagetti  </p><p><a href="https://www.yelp.com/biz/corkys-ribs-and-bbq-memphis-2">Corky’s Ribs &amp; BBQ</a> – Ribs and Catfish  </p><p><a href="https://www.yelp.com/biz/cozy-corner-restaurant-memphis-20">Cozy Corner Restaurant</a> – Cornish hen and rib tips  </p><p><a href="http://www.commissarybbq.com">Commissary BBQ</a> – Germantown</p><p><a href="https://www.yelp.com/biz/leonards-pit-barbecue-memphis">Leonard’s Pit Barbecue</a> - buffet  </p><p><a href="https://www.yelp.com/biz/interstate-barbecue-memphis">Interstate Barbecue</a> – BBQ spaghetti  </p><p><a href="https://www.yelp.com/biz/one-and-only-bbq-memphis-4">One &amp;  Only BBQ</a>  </p><p><a href="https://www.yelp.com/biz/toms-barbecue-and-deli-memphis-3">Tom’s Barbecue and Deli</a> – rib tips  Featured on Diners Drive Ins and Dives</p><p><em>TOURIST BBQ</em> <a href="https://www.yelp.com/biz/charlie-vergos-rendezvous-memphis">Rendezvous BBQ</a> – they don’t slow smoke their ribs, they grill them  </p>'
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


