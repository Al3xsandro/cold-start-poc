from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/logout', views.user_logout, name="logout"),
    path('', views.index, name="index"),
    path('mylist', views.mylist, name="mylist"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
