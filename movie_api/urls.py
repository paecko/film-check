from django.urls import path
from movie_api.views import authentication_views, movie_views

app_name = "movie_api"
urlpatterns = [
    path("", movie_views.index, name="index"),
    path("login/", authentication_views.login, name="login"),
    path("logout/", authentication_views.logout, name="logout"),
    path("callback/", authentication_views.callback, name="callback"),
    path("movies/<movie_pk>/", movie_views.detailed_movie, name="detailed_movie"),
    path("search/", movie_views.search, name="search_results"),
    path("my_watched_movies/", movie_views.my_watched_movies, name="my_watched_movies"),
    path("my_watch_list/", movie_views.my_watch_list, name="my_watch_list"),

    path("movies/<movie_pk>/save_rating/", movie_views.save_rating, name="save_rating"),
    path("movies/<movie_pk>/check/", movie_views.check_movie, name="check_movie"),
    path("movies/<movie_pk>/add_to_watch_list/", movie_views.add_to_watch_list, name="add_to_watch_list"),
]