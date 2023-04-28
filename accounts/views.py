from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# from authentication.auth import CustomerAuthentication
from accounts.forms import  UserRegisterForm, ProjectForm
from rest_framework.permissions import  IsAuthenticated
from django.views.generic import TemplateView, View, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import redirect, render
from accounts.models import AppToken,Project
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from accounts.serializers import UserRegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import mixins
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy


class Index(TemplateView):
    """
    this view show the index page 
    """
    template_name = 'accounts/index.html'
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            token :RefreshToken= RefreshToken.for_user(request.user)
            self.request.COOKIES['access_token'] = 'Bearer'+'  '+str(token.access_token)
            self.request.COOKIES['refresh_token'] = str(token)
            self.request.session['access_token'] = 'Bearer'+'  '+str(token.access_token)
            self.request.session['refresh_token'] = str(token)
            self.request.session.modified = True
        return super().get(request, *args, **kwargs)
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


class ProjectsView(mixins.LoginRequiredMixin, ListView):
    model  = Project
    template_name = "accounts/project_list.html"
    paginate_by = 10

    def get_queryset(self):
        return self.request.user.projects.all()

class CreateProjectsView(mixins.LoginRequiredMixin, CreateView):
    form_class = ProjectForm
    template_name = "accounts/create_project.html"
    success_url = reverse_lazy('projects')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return redirect('projects')

class ProjectDetailView(mixins.LoginRequiredMixin, DetailView):
    model = Project
    extra_context = {}

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if self.request.user == obj.user: 
            self.extra_context['token'] = self.request.session.get('access_token')
            return super().get(request, *args, **kwargs)
        else:
            raise PermissionDenied

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
    
class ProjectUpdate(mixins.LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "accounts/project_edit.html"

    def form_valid(self, form):
        instance = form.save()
        return redirect("project_detail", pk=self.get_object().pk)

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if self.request.user == obj.user:  # only org creator can update organization
            return super().get(request, *args, **kwargs)

        else:
            raise PermissionDenied
        
