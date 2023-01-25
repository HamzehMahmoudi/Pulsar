from django.urls import path
from accounts import api


urlpatterns = [
    path('user/projects/', api.ProjectsView.as_view()),
]