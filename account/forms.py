from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from .models import UserExtraInfo, User


class AvatarWidget(forms.ClearableFileInput):
    template_name = 'account/profile/avatar_widget.html'
    clear_checkbox_label = _("Clear Avatar")
    initial_text = ''

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserExtraInfo
        fields = ['first_name' , 'last_name'  , 'birthdate' , 'gender' , 'avatar']
        widgets = {
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'birthdate': forms.DateInput(attrs={'class': 'form-control' , 'type': 'date'}),
            'avatar': AvatarWidget(attrs={'class': 'form-control-file'}),
        }

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}) ,
        validators=[validate_password]
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise ValidationError("Passwords do not match")

        return cleaned_data


class LoginForm(AuthenticationForm):
    """
    add "Remember Me" checkbox to it
    """

    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())

class SignUpForm (UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        """
          It doesn't use create_user from UserManager by default
        """
        cleaned_data = self.cleaned_data

        if not commit:
            user = super().save(commit=False)
            user.set_password(cleaned_data["password1"])
            return user

        # replace 'password' field instead of password1 and password2
        # and create random activation code
        password = cleaned_data.pop('password1')
        cleaned_data.pop('password2')
        cleaned_data.update(
            {
                'password' : password ,
                'activation_code' : get_random_string(72)
            }
        )

        user = User.objects.create_user(**cleaned_data)
        return user


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )