from django.urls import path
from .views import IndexTemplateView ,HomeOrTaskRedirectView

app_name = 'home'

urlpatterns = [
    path("", HomeOrTaskRedirectView.as_view() , name= 'redirect_view'),
    path("home/", IndexTemplateView.as_view() , name= 'home_view'),

]