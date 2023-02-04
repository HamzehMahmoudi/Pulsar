from rest_framework.views import APIView
from rest_framework.response import Response
# from authentication.auth import CustomerAuthentication
from accounts.forms import  UserRegisterForm
from rest_framework.permissions import  IsAuthenticated
from django.views.generic import TemplateView
from django.shortcuts import redirect, render
class Index(TemplateView):
    """
    this view show the index page 
    """
    template_name = 'accounts/index.html'
    
class About(TemplateView):
    """
    this view show the index page 
    """
    template_name = 'accounts/about.html'


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "accounts/register.html", {"form": form})
    

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
        return Response(data={"error": "name is required"}, status=400)
   