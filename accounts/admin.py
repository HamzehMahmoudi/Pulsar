from django.contrib import admin
from accounts.models import User, Project, ProjectUser, AppToken
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'is_active']
    list_filter = ['is_staff']
    search_fields = ['username', 'email']
    exclude = ['password', 'groups', 'user_permissions']

admin.site.register([Project, ProjectUser, AppToken])