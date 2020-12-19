from django.contrib import admin
from .models import User, Blog
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    pass

admin.site.register(User, CustomUserAdmin)
admin.site.register(Blog)
