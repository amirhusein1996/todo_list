from django.urls import path
from .views import AboutUsTemplateView

app_name = 'about_us'

urlpatterns= [
    path('', AboutUsTemplateView.as_view() , name= 'about_us_view')
]