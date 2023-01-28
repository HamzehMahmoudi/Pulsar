from rest_framework.views import APIView
from rest_framework.response import Response
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
    

class ProjectsView(APIView):
    permission_classes = [IsAuthenticated]
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
        return Response(data=res, status=200)
    
    def post(self, request):
        user = request.user
        data = request.data
        name = data.get('name', None)
        if name is not None:
            project = user.projects.create(name=name)
            return Response(data={"id": project.id}, status=201)
        else:
            return Response(data={"error": "name is required"}, status=400)
    

        
        