from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from authentication.auth import CustomerAuthentication
from rest_framework.permissions import IsAuthenticated
from chat.models import Chat, ChatTypes
from chat.serializers import ChatSerializer
from accounts.models import AppToken, ProjectUser
from django.utils.translation import gettext_lazy as _
class ChatsAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer

    def get_queryset(self):
        request = self.request
        user = request.user
        project = request.GET.get('project')
        user_id = request.GET.get('user')
        project = user.projects.filter(pk=project).first()
        if project is None:
            return Chat.objects.none()
        project_user, created = project.users.get_or_create(identifier=user_id)
        return project_user.chats.all()

class GetPvAPI(APIView):
    def post(self, request):
        user = request.user
        token = request.data.get('token')
        token = AppToken.objects.filter(key=token).first()
        if token is None:
            return Response(data={'error': _('invalid token')})
        if not token.is_valid():
            return Response(data={'error': _('invalid token')})
        project = user.projects.filter(pk=token.project_id).first()
        if project is None:
            return Response(data={'error': _('invalid token')})
        user_id = request.data.get('cuser')
        other_user = request.data.get('ouser')
        project_user, created = project.users.get_or_create(identifier=user_id)
        other_project_user, ocreated = project.users.get_or_create(identifier=other_user)
        chat = Chat.objects.create(chat_type=ChatTypes.PV, project=project)
        chat.members.add(project_user, other_project_user)
        chat.save()
        return Response(data={"chat_id":chat.id})
        
        
    