from django.urls import path
from chat import api


urlpatterns = [
    path('', api.ChatsAPI.as_view()),
    path('pv', api.GetPvAPI.as_view()),   
]
