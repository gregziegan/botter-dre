import sys
from django.core.management.base import BaseCommand, CommandError
from botterdre_app.models import Lyrics, GeneratedSong
import re
import random
from pyquery import PyQuery
import datetime

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('song_length', type=int)

    def handle(self, *args, **options):
        try:
            self.makeGeneratedSong(options['song_length'])

        except Lyrics.DoesNotExist:
            raise CommandError('Lyrics "%s" does not exists' % lyric_id)


    def makeGeneratedSong(self, length):

        linking_words = ['to', 'and', 'also', 'then', 'like', 'as', 'but'
                        'still', 'or', 'if', 'until', 'the', 'a', 'my', 'his'
                        'have']

        randGeneratedSong = random.choice(Lyrics.objects.all()).words
        words = randGeneratedSong.split()
        ab = words[:2]
        a, b = (ab[0], ab[1])

        song = a + ' ' + b + ' '
        c = ''

        i, bad_word_count = 0, 0
        while i < length:

            next_song = random.choice(Lyrics.objects.filter(words__contains=' %s ' % b)).words.split()
            if bad_word_count > 15:
                song += '\n'
                b = random.choice(next_song[:-1])
            if next_song[-1] == b:
                bad_word_count += 1
                continue

            for j in range(len(next_song)):
                if next_song[j] == b:
                    c = next_song[j + 1]
                    if c.islower() or len(c) == 1:
                        song += c + ' '
                    else:
                        song += '\n' + c + ' '
                    b = c[:]
                    i += 1
                    bad_word_count = 0
                    break

        # Format weird endings
        if song[-1] == ',' or song[-1] == ';':
            song = song[:-1]

        song_words = song.split()
        capitals = re.compile(r'([A-Z]\w+)\s+')
        capitalized_words = re.findall(capitals, song)

        if len(capitalized_words) > 1:
            first_word = random.choice(capitalized_words[:-1])
        elif len(capitalized_words) == 1:
            first_word = capitalized_words[0]
        else:
            first_word = random.choice(song_words[:-7])

        title_index = 0
        for k in range(len(song_words)):
            if first_word == song_words[k]:
                title_index = k
                break

        title_words = song_words[title_index:title_index + random.randrange(3, 7)]
        title = ' '.join(title_words)

        title = title[0].upper() + title[1:]
        s = GeneratedSong(title=title, lyrics=song)
        s.save()

