from django.urls import path
from accounts import api,views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('user/projects/', api.ProjectsView.as_view()),
    path('user/projects/token/<int:pk>/', api.GenerateToken.as_view(), name='get_token'),
    path("login", auth_views.LoginView.as_view(
        template_name="accounts/login.html"), name="login"),
    path("logout", auth_views.LogoutView.as_view(
        template_name="accounts/logout.html"), name="logout"),
    path("register", views.register, name="register"),
    path("api/register", api.CreateUserAPI.as_view(), name="registerapi"),
    path("projects", views.ProjectsView.as_view(), name="projects"),
    path("projects/create/", views.CreateProjectsView.as_view(), name="create_project"),
    path("project/<int:pk>", views.ProjectDetailView.as_view(), name="project_detail"),
    path("project/edit/<int:pk>/", views.ProjectUpdate.as_view(), name="project_edit"),
]
