from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("post/<str:slug>/", views.details, name="details"),
    path("post/<str:slug>/edit", views.edit, name="edit"),
    path("post/<str:slug>/delete", views.delete, name="delete"),
    path("write/", views.write, name="write"),
]
