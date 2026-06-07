from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.home, name="home"),
    path("watches/", views.watch_list, name="watch_list"),
    path("watches/<int:watch_id>", views.watch_detail, name="watch_detail"),
]
