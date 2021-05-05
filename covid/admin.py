from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

# Register your models here.


class CHPInline(admin.StackedInline):
    model = CHP_User
    can_delete = False
    verbose_name_plural = 'CHP Users'

class UserAdmin(BaseUserAdmin):
    inlines = (CHPInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Case)
admin.site.register(Event)
admin.site.register(Attendance)