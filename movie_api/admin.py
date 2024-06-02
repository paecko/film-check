from django.contrib import admin
from .models import Movie, CheckedMovie, WatchListMovie

admin.site.register(Movie)
admin.site.register(CheckedMovie)
admin.site.register(WatchListMovie)
