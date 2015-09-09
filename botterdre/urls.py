"""botterdre URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from botterdre_app import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^lyrics/(\d+)/', views.lyrics, name='lyrics'),
    url(r'generate-song/', views.generate_song, name='generate_song'),
    url(r'^about/', views.about, name='about'),
    url(r'^admin/', include(admin.site.urls))
]
