from django.contrib import admin
from .models import User, Blog, Comment, Like
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    pass

admin.site.register(User, CustomUserAdmin)
admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Like)
