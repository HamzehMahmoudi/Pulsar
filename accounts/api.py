from rest_framework.views import APIView
from rest_framework.response import Response
# from authentication.auth import CustomerAuthentication
from accounts.forms import  UserRegisterForm
from rest_framework.permissions import  IsAuthenticated
from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from accounts.models import AppToken
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from accounts.serializers import UserRegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
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

class CreateUserAPI(APIView):
    def post(self, request):
        data =request.data
        serilized_data = UserRegisterSerializer(data=data)
        if serilized_data.is_valid():
            validated_data = serilized_data.validated_data
            instance = serilized_data.create(validated_data=validated_data)
            token = RefreshToken.for_user(instance)
            return Response(data={"access": str(token.access_token), "refresh": str(token)})
        else:
            return Response(data=serilized_data.errors, status=400)

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
    
class GenerateToken(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        user = self.request.user
        project = user.projects.filter(pk=pk).first()
        if project is not None:
            token = AppToken.objects.create(project=project, expire_on=timezone.now()+timezone.timedelta(days=30))
            return Response(status=200, data={"token": token.key})
        return Response(status=400, data={"error": _("invalid project_id")})
    
    def get(self, request, pk):
        user = self.request.user
        project = user.projects.filter(pk=pk).first()
        if project is not None:
            token = AppToken.objects.filter(project=project, expire_on__gte=timezone.now()).first()
            return Response(status=200, data={"token": token.key})
        return Response(status=400, data={"error": _("invalid project_id")})
