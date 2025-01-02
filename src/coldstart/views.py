from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    is_first_access = request.user.is_first_access
    if not is_first_access:
        return redirect('mylist')
    
    return render(request, 'index.html', {})

@login_required
def mylist(request):
    is_first_access = request.user.is_first_access
    if is_first_access:
        return redirect('index')
    
    movies = request.user.mymovielist.all()
    return render(request, 'mylist.html', { "movies": movies })

@login_required
def user_logout(request):
    logout(request)
    return render(request, "index.html", {})