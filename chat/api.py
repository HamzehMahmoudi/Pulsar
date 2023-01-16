from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

# from authentication.auth import CustomerAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.models import Project
from chat.serializers import ChatSerializer
    
class ChatsAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer

    def list(self, request):
        user = request.user
        project_id = request.GET.get('project')
        user_id = request.GET.get('user')
        project = user.projects.filter(pk=project_id).last()
        if project is not None:
            project_user = project.users.filter(id=user_id).last()
            if project_user is not None:
                chats = project_user.chats.all()
                page = self.paginate_queryset(chats)
                if page is not None:
                    serializer = self.get_serializer(page, many=True)
                    return self.get_paginated_response(serializer.data)
                serializer = self.get_serializer(chats, many=True)
                return Response(data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)