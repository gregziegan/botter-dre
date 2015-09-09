from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from botterdre_app.models import Lyrics
import re
import requests
from pyquery import PyQuery
import threading
from urllib.parse import urljoin

domain = 'http://www.lyrics.com/tophits/home_genres/'

exitFlag = 0

class worker(threading.Thread):
    def __init__(self, threadID, name, genre):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.genre = genre
    def run(self):
        getSongs(self.name, self.genre)

def getSongs(threadName, genre):

    j = 0
    while j <= 200:
        if exitFlag:
            thread.exit()
        path = '{index}/{genre}'.format(index=j, genre=genre)
        url = urljoin(domain, path)
        findLyrics(url)
        j += 30

def findLyrics(url):
    html = requests.get(url).text
    links = re.findall(r'<td[^>]*?><a href="([^"]+?)"', html)

    for link in links:
        html = requests.get(urljoin(domain, link)).text
        pq = PyQuery(html)
        if pq('#lyrics'):
            lyrics = pq('#lyrics').text()
        else:
            lyrics = pq('#lyric_space').text()
        if lyrics.find('---') != -1:
            lyrics = lyrics[:lyrics.find('---')]
        if len(lyrics) < 200:
            continue
        try :
            l = Lyrics.objects.create(words=lyrics)
        except IntegrityError as e:
            continue


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            threadID = 1
            genres = {'Alternative': 20, 'Christian': 22, 'Country': 6, 'Dance': 17,
                      'Hip Hop': 18, 'Pop': 14, 'Soul': 15, 'Rock': 21}
            for genre, genreId in genres.items():
                threadName = 'Thread-' + str(threadID)
                thread = worker(threadID, threadName, genreId)
                thread.start()
                threadID += 1

        except KeyboardInterrupt:
            exitFlag = 1
