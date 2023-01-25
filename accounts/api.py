from rest_framework.views import APIView
# from authentication.auth import CustomerAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views import View
from django.http import HttpResponse, JsonResponse
class Index(View):
    permission_classes = [AllowAny]

    def get(self, request):
        return HttpResponse("<title>pulsar</title><h1> wellcome to pulsar :) </h1><br><p>there will be more content soon ... </p>")

class Dashboard(View):
    ...
    

class ProjectsView(View):
    def get(self, request):
        user = request.user
        res = []
        projects = user.projects.all().values('id', 'name').iterator()
        for p in projects:
            p_data = {
                "id": p['id'],
                "name": p['name']
            }
            res.append(p_data)
        return JsonResponse(data=res, safe=False)
    
class ChatsAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        
        