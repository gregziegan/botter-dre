from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.http import Http404
from django.conf import settings
from .models import GeneratedSong
from django.core.management import call_command
from . import utils

DEFAULT_SONG_LENGTH = 150

def home(request, template_name="home.html"):
    recent_songs = GeneratedSong.objects.order_by('-id')[:10]

    return render(request, template_name, {'recent_songs': recent_songs})

def about(request):
    return render(request, 'about.html')

def generate_song(request):
    if request.method == 'POST':
        call_command('generatesong', str(DEFAULT_SONG_LENGTH))
        song_id = GeneratedSong.objects.order_by('-id')[0].id
        return redirect(reverse('lyrics', args=[song_id]))

def lyrics(request, song_id):
    song = GeneratedSong.objects.get(id=song_id)
    song_lyrics = song.lyrics.split('\n')
    return render(request, 'lyrics.html', {'song_title': song.title, 'song': song, 'song_lyrics': song_lyrics})


def search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = utils.get_query(query_string, ['title', 'lyrics',])

        found_entries = GeneratedSong.objects.filter(entry_query).order_by('-date_created')

    return render(request, 'search_results.html', {'query': query_string, 'songs': found_entries})
