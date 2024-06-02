from django.shortcuts import render, get_object_or_404, redirect
from movie_api.models import Movie, CheckedMovie, WatchListMovie
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q

import json

def index(request):
    recent_movies = Movie.objects.order_by('-date_added')[:12]
    return render(request, 'movie_api/home.html', {'recent_movies': recent_movies})

def detailed_movie(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    context = {"movie": movie, "movie_checked": False, "in_watch_list": False}
    if request.session.get('user'):
        user = User.objects.get(email=request.session.get('user').get('userinfo').get('email'))
        try:
            checked_movie = CheckedMovie.objects.get(User=user, Movie=movie)
            context['movie_checked'] = True

            if checked_movie.rating is not None:
                context['rating'] = checked_movie.rating
            else:
                context['rating'] = -1

        except (KeyError, CheckedMovie.DoesNotExist):
            context['movie_checked'] = False

        if WatchListMovie.objects.filter(User=user, Movie=movie).exists():
            context['in_watch_list'] = True

    return render(request, "movie_api/detailed_movie.html", context)

def search(request):
    if request.method == 'GET':
        query = request.GET['q']

        movies = Movie.objects.filter(Q(title__icontains=query) | Q(title__search=query)).order_by('-imdb_rating', '-date_added')
        paginator = Paginator(movies, 8)
        page_number = request.GET.get("page")
        page_movies = paginator.get_page(page_number)

        return render(request, "movie_api/search_results.html", {'movies': page_movies, 'query': query})
    else:
        return render(request, 'movie_api/search_results.html')
  

def my_watched_movies(request):
    try:
        user = get_object_or_404(User, email=request.session.get('user').get('userinfo').get('email'))
    except Http404:
        return redirect('movie_api:index')

    checked_movie_objects = CheckedMovie.objects.filter(User=user).order_by('-checked_on')
    movie_ids = checked_movie_objects.values_list('Movie__id', flat=True).distinct()
    # this filter does not return objects based on the order in movie_ids
    watched_movies = Movie.objects.filter(id__in=movie_ids)

    # sort by converting to list and using lambda function that compares ids from original ids list.
    watched_movies = list(watched_movies)
    movie_ids = list(movie_ids)
    watched_movies.sort(key=lambda movie: movie_ids.index(movie.id))

    paginator = Paginator(watched_movies, 8)
    page_number = request.GET.get("page")
    page_movies = paginator.get_page(page_number)

    return render(request, 'movie_api/my_watched_movies.html', 
                        {'watched_movies':page_movies})

def my_watch_list(request):
    try:
        user = get_object_or_404(User, email=request.session.get('user').get('userinfo').get('email'))
    except Http404:
        return redirect('movie_api:index')

    watch_list_movie_objects = WatchListMovie.objects.filter(User=user).order_by('-added_on')
    movie_ids = watch_list_movie_objects.values_list('Movie__id', flat=True).distinct()
    # this filter does not return objects based on the order in movie_ids
    watch_list_movies = Movie.objects.filter(id__in=movie_ids)

    # sort by converting to list and using lambda function that compares ids from original ids list.
    watch_list_movies = list(watch_list_movies)
    movie_ids = list(movie_ids)
    watch_list_movies.sort(key=lambda movie: movie_ids.index(movie.id))

    paginator = Paginator(watch_list_movies, 8)
    page_number = request.GET.get("page")
    page_movies = paginator.get_page(page_number)

    return render(request, 'movie_api/my_watch_list.html', 
                        {'watch_list_movies':page_movies})

def check_movie(request, movie_pk):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, pk=movie_pk)
        user = get_object_or_404(User, email=request.session.get('user').get('userinfo').get('email'))
        response_data = {'movie_checked': None}

        try:
            CheckedMovie.objects.get(User=user, Movie=movie).delete()
            response_data['movie_checked'] = False
            print("unchecking movie")
        except (KeyError, CheckedMovie.DoesNotExist):
            print("movie not checked. now checking")
            checked_movie = CheckedMovie(User=user, Movie=movie)
            checked_movie.save()
            response_data['movie_checked'] = True

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

def add_to_watch_list(request, movie_pk):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, pk=movie_pk)
        user = get_object_or_404(User, email=request.session.get('user').get('userinfo').get('email'))
        response_data = {'in_watch_list': None}

        try:
            WatchListMovie.objects.get(User=user, Movie=movie).delete()
            response_data['in_watch_list'] = False
            print("removing from watch list")
        except (KeyError, WatchListMovie.DoesNotExist):
            new_watch_list_movie = WatchListMovie(User=user, Movie=movie)
            new_watch_list_movie.save()
            response_data['in_watch_list'] = True
            print("Saving movie to watch list....")

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

def save_rating(request, movie_pk):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, pk=movie_pk)
        user = get_object_or_404(User, email=request.session.get('user').get('userinfo').get('email'))
        response_data = {'movie_checked': True}
        rating = int(request.POST['rating'])
        try:
            checked_movie = CheckedMovie.objects.get(User=user, Movie=movie)
            if rating >= 0 and rating <= 4:
                checked_movie.rating = rating
            else:
                checked_movie.rating = None
            checked_movie.save() 
        except Exception as e:
            response_data['movie_checked'] = False
            print(e)

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )