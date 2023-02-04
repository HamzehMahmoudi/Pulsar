from channels.middleware import BaseMiddleware
from accounts.models import AppToken
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser
from urllib.parse import parse_qs
from asgiref.sync import sync_to_async


async def get_token(token_key):
    return AppToken.objects.filter(key=token_key).alast()

def get_headers(scope):
    scope_headers = scope.get('headers', [])
    headers = { key.decode(): value.decode() for key , value in scope_headers}
    return headers
        
    
class TokenAuthentication(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)
    
    @sync_to_async
    def populate_scope(self ,scope):
        qs = parse_qs(scope['query_string'].decode())
        headers = get_headers(scope=scope)
        auth = headers.get('auth', None)
        p_uid = qs.get('uid', [None])[0]
        token = AppToken.objects.filter(key=auth).last()
        scope['project'] = None
        scope['project_user'] = None
        if token is not None:
            if token.is_valid():
                project = token.project
                scope['project'] = project
                project_user = project.users.filter(identifier=p_uid).last()
                scope['project_user'] = project_user
        return scope

    async def __call__(self, scope, receive, send):
        scope = await self.populate_scope(scope)
        return await super().__call__(scope, receive, send)           
 