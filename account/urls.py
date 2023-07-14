from django.contrib.auth.views import LoginView
from django.urls import path
from .views import EditProfileView, SignInView, SignUpView, ResetPasswordRequestView, SignOutView, \
    ResetPasswordConfirmView, ActivationView

app_name = 'account'

registration_urls =[
    path('log-in/', SignInView.as_view() , name ='login_view'),
    path('log-out/', SignOutView.as_view(), name='logout_view') ,
    path('sign-up/' , SignUpView.as_view() , name= 'sign_up_view'),
    path('reset-password/' , ResetPasswordRequestView.as_view() , name="reset_password_request_view"),
    path('activation/<str:activation_code>/', ActivationView.as_view(), name='activation_view'),
    path('reset-password-confirmation/<str:activation_code>/',ResetPasswordConfirmView.as_view() , name='reset_password_confirmation_view')

]

other_urls = [
    path('edit-profile', EditProfileView.as_view() , name='edit_profile_view'),
]

urlpatterns = registration_urls + other_urls
