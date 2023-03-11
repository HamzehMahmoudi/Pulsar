from django.urls import path
from payment import views

urlpatterns = [

    path("pay/", views.Pay.as_view(), name="callback-gateway")
]
