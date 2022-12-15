# from rest_framework.authentication import TokenAuthentication
# from .models import AppToken
# from rest_framework.exceptions import AuthenticationFailed
# import pytz
# from django.utils import timezone
# from datetime import datetime

# class CustomerAuthentication(TokenAuthentication):
#     keyword = 'Token'
#     model = AppToken
#     def authenticate_credentials(self, key, request=None):
#             models = self.get_model()

#             try:
#                 token = models.objects.select_related("company").get(key=key)
#             except models.DoesNotExist:
#                 raise AuthenticationFailed(
#                     {"error": "Invalid or Inactive Token", "is_authenticated": False}
#                 )

#             if not token.company.is_active:
#                 raise AuthenticationFailed(
#                     {"error": "Invalid company", "is_authenticated": False}
#                 )

#             utc_now = timezone.now()
#             utc_now = utc_now.replace(tzinfo=pytz.utc)

#             if utc_now > token.expire_on:
#                 raise AuthenticationFailed(
#                     {"error": "Token has expired", "is_authenticated": False}
#                 )
#             return token.company, token
