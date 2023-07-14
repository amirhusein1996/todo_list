from django.contrib import admin
from .models import ContactUsMessage

@admin.register(ContactUsMessage)
class ContactUsModelAdmin(admin.ModelAdmin):
    pass