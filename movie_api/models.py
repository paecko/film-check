from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Movie(models.Model):
    title = models.CharField(max_length=5000)
    year = models.CharField(max_length=5000, null=True)
    released = models.CharField(max_length=5000, null=True)
    runtime = models.CharField(max_length=5000, null=True)
    poster = models.CharField(max_length=5000, null=True)
    genres = models.CharField(max_length=5000, null=True)
    director = models.CharField(max_length=5000, null=True)
    actors = models.CharField(max_length=5000, null=True)
    plot = models.CharField(max_length=5000, null=True)
    language = models.CharField(max_length=5000, null=True)
    country = models.CharField(max_length=5000, null=True)
    type = models.CharField(max_length=5000, null=True)
    imdb_id = models.CharField(max_length=5000, null=True)
    imdb_votes = models.IntegerField(null=True)
    imdb_rating = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class CheckedMovie(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True)
    checked_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.Movie.title} checked by {self.User.email} on {self.checked_on}"

class WatchListMovie(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    added_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.Movie.title} added by {self.User.email} on {self.added_on}"
        