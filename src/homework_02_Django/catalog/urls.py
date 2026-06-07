from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.home, name="home"),
    path("watches/", views.watch_list, name="watch_list"),
    path("watches/add/", views.watch_create, name="watch_create"),
    path("watches/<int:watch_id>", views.watch_detail, name="watch_detail"),
    path("watches/<int:watch_id>/delete/", views.watch_delete, name="watch_delete"),
]
