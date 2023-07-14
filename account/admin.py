from django.contrib import admin
from .models import User , UserExtraInfo

@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    pass


@admin.register(UserExtraInfo)
class UserExtraInfoModelAdmin(admin.ModelAdmin):
    pass