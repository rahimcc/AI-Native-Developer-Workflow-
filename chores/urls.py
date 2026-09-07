from django.urls import path

from . import views

app_name = "chores"

urlpatterns = [
    path("", views.chore_list, name="chore_list"),
    path("chores/add/", views.chore_add, name="chore_add"),
    path("chores/<int:pk>/edit/", views.chore_edit, name="chore_edit"),
    path("chores/<int:pk>/delete/", views.chore_delete, name="chore_delete"),
    path("chores/<int:pk>/complete/", views.chore_complete, name="chore_complete"),
    path("members/", views.member_list, name="member_list"),
    path("members/add/", views.member_add, name="member_add"),
    path("members/<int:pk>/edit/", views.member_edit, name="member_edit"),
    path("members/<int:pk>/delete/", views.member_delete, name="member_delete"),
]
