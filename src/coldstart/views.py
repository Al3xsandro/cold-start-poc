from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
import json

from movies.views import recommend_movies, create_user_list


@login_required
def index(request):
    is_first_access = request.user.is_first_access
    if not is_first_access:
        return redirect("mylist")

    return render(request, "index.html", {})


@login_required
def mylist(request):
    is_first_access = request.user.is_first_access
    if is_first_access:
        return redirect("index")

    (recommended_movies, voted_movies, my_movies) = recommend_movies(request.user)
    return render(
        request,
        "mylist.html",
        {
            "recommended_movies": recommended_movies,
            "voted_movies": voted_movies,
            "my_movies": my_movies,
        },
    )


@login_required
def user_logout(request):
    logout(request)
    return render(request, "index.html", {})


def submit_genres(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            selected_genres = data.get("genres", [])
            favorites = data.get("favorites", [])

            if len(selected_genres) < 3:
                return JsonResponse(
                    {"error": "You must select at least 4 genres."}, status=401
                )

            user = request.user
            user.is_first_access = False
            user.save()

            create_user_list(user, selected_genres, favorites)

            return JsonResponse({"message": "Genres submitted successfully!"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


def rate_movie():
    return
