from rest_framework.views import APIView
# from authentication.auth import CustomerAuthentication
from rest_framework.permissions import AllowAny
from django.views import View
from django.http import HttpResponse, JsonResponse
class testEndpoint(View):
    permission_classes = [AllowAny]

    async def get(self, request):
        return HttpResponse("<title>pulsar</title><h1> wellcome to pulsar :) </h1><br><p>there will be more content soon ... </p>")

class Dashboard(View):
    ...
    

class GetProjects(View):
    ...
    