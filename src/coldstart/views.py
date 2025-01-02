from django.shortcuts import render
from django.contrib.auth import logout

def index(request):
    return render(request, 'index.html', {})

def mylist(request):
    movies = request.user.mymovielist.all()
    return render(request, 'mylist.html', { "movies": movies })

def user_logout(request):
    logout(request)
    return render(request, "index.html", {})