from django.contrib import admin
from ninja_knox import models


@admin.register(models.AuthToken)
class AuthTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'created_at', 'expiry']
