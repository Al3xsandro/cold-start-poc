from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("accounts/logout", views.user_logout, name="logout"),
    path("", views.index, name="index"),
    path("submit-genres/", views.submit_genres, name="submit_genres"),
    path("mylist", views.mylist, name="mylist"),
    path("rate-movie/<int:movie_id>/", views.rate_movie, name="rate_movie"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
