from rest_framework.generics import ListAPIView

# from authentication.auth import CustomerAuthentication
from rest_framework.permissions import IsAuthenticated
from chat.models import Chat
from chat.serializers import ChatSerializer
    
class ChatsAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer
    
    def get_queryset(self):
        request = self.request
        user = request.user
        project_id = request.GET.get('project')
        user_id = request.GET.get('user')
        project = user.projects.filter(pk=project_id).first()
        if project is None:
            return Chat.objects.none()
        project_user = project.users.filter(identifier=user_id).first()
        if project_user is None:
            return Chat.objects.none()
        return project_user.chats.all()