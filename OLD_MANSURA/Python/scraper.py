import math
import shutil
import sys
import os
import hashlib
import requests
from bs4 import BeautifulSoup
import re

'''
TASKS:
1. SCRAPE WEBSITE FOR A BUNCH OF LINKS
2. TEST AUTOMATED INSERT WITH A FEW LINKS AND SEE IF THEY SHOW UP
3. IF WORKING, AUTOMATE INSERTING MY ENTIRE TIKTOK PAGE 
4. IF WORKS, DO THE SAME ON LIVE, AS WELL 

'''

def WRITE_TO_FILE(string):
    # print(string)
    with open('/root/mansura/Notes/TODO/PAGE LINKS/tiktok_links.txt', 'a') as f:
        # print(string)
        f.write(string)

def OPEN_TO_FILE():
    # FIRST STEP IS GO TO THE PAGE AND GRAB THE HTML TAG WITHT THE VIDEOS, SCROLL DOWN TO GET ALL
    with open('/root/mansura/Notes/TODO/PAGE HTML/mazinosarchive.txt', 'r') as f:
        files = f.read()
        x = re.findall("https://www.tiktok.com/@mazinosarchive/video/[0-9]{19}", files)
        # print(x)
        for i in x:
            WRITE_TO_FILE(str(i) + "\n")    

def SCRAPE_YOUTUBE_CHANNEL(channel_link):
    pass

def SCRAPE_TIKTOK_PAGE(channel_link):
    pass

\




