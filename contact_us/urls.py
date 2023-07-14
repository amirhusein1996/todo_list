from django.urls import path
from .views import *

app_name = 'contact_us'

urlpatterns = [
    path('', ContactUsFormView.as_view() , name = 'contact_us_view'),
]