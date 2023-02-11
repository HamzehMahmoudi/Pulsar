from django.urls import path
from accounts import api
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('user/projects/', api.ProjectsView.as_view()),
    path('user/projects/<int:pk>/', api.GenerateToken.as_view()),
    path("login", auth_views.LoginView.as_view(
        template_name="accounts/login.html"), name="login"),
    path("logout", auth_views.LogoutView.as_view(
        template_name="accounts/logout.html"), name="logout"),
    path("register", api.register, name="register"),
    path("api/register", api.CreateUserAPI.as_view(), name="registerapi"),
]
