from rest_framework.generics import ListAPIView

# from authentication.auth import CustomerAuthentication
from rest_framework.permissions import IsAuthenticated
from chat.models import Chat
from chat.serializers import ChatSerializer

class ChatsAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer

    def get_queryset(self):
        from accounts.models import AppToken
        request = self.request
        user = request.user
        token = request.GET.get('token')
        token = AppToken.objects.filter(key=token).first()
        if token is None:
            return Chat.objects.none()  
        user_id = request.GET.get('user')
        project = user.projects.filter(pk=token.project_id).first()
        if project is None:
            return Chat.objects.none()
        project_user, created = project.users.get_or_create(identifier=user_id)
        return project_user.chats.all()
