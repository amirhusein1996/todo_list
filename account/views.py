from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from django.views import View
from django.views.generic import UpdateView, CreateView

from .forms import ProfileForm, ChangePasswordForm, LoginForm, SignUpForm, ResetPasswordForm
from .mixins import SendMailMixin, RedirectAuthenticatedUserMixin
from .models import UserExtraInfo, User


class EditProfileView(UpdateView):
    template_name = 'account/profile/edit_profle.html'
    model = UserExtraInfo  # Specify the model attribute initially, it may change
    success_url = reverse_lazy("home:redirect_view")

    def get_form_class(self):
        if self.model == User:
            self.form_class = ChangePasswordForm
            return ChangePasswordForm
        self.form_class = ProfileForm
        return ProfileForm

    def get_object(self, queryset=None):
        form_identifier = self.request.POST.get("form_identifier")
        if form_identifier == "change_password":
            self.model = User
            return self.request.user
        return get_object_or_404(klass=self.model, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = self.get_form()

        if form.__class__ == ProfileForm:
            profile_form = form
            password_form = ChangePasswordForm()
        else:
            profile_form = ProfileForm()
            password_form = form

        context.update({
            'profile_form': profile_form,
            'password_form': password_form
        })

        return context

    def get_form(self, form_class=None):
        kwargs = self.get_form_kwargs()
        form_class = self.get_form_class()
        if form_class == ProfileForm:
            return form_class(**kwargs)

        """
        ChangePasswordForm is Not ModelForm,
        so doesn't need instance
        """
        kwargs.pop('instance', None)
        return form_class(**kwargs)

    def form_valid(self, form):
        if form.__class__ == ProfileForm:
            return super().form_valid(form)

        cd = form.cleaned_data

        user = authenticate(
            request=self.request,
            username=self.request.user.username,
            password=cd.get("current_password")
        )

        if user is not None:
            try:
                user.set_password(cd.get('new_password'))
                user.save()
                """It will log the user out after changing password,
                we try to keep him logged in
                """
                login(self.request, user)
                return redirect(self.get_success_url())
            except:
                form.add_error('new_password',
                               'validation error')  # it's better to show same errors to user for security reason

        return self.render_to_response(self.get_context_data())


class SignOutView(LogoutView):
    template_name = 'account/registration/logout_message.html'



class SignInView(RedirectAuthenticatedUserMixin,LoginView):
    template_name = 'account/registration/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        has_remember_me = form.cleaned_data.get('remember_me')

        if not has_remember_me:
            self.request.session.set_expiry(0)  # don't remember user
            self.request.session.modified = True

        return super().form_valid(form)


class SignUpView(RedirectAuthenticatedUserMixin,SendMailMixin, CreateView):
    form_class = SignUpForm
    template_name = 'account/registration/signup.html'

    email_template_name = 'account/email_templates/confirm_email.html'
    subject = "Confirm Email"

    def form_valid(self, form):

        new_user = form.save()
        try:
            """
            Note : It's better to use transaction atomic that if sending email failed, 
            prevent to create user.
            """
            self.send_mail(
                to=new_user.email,

                context={
                    'username': new_user.username,
                    'confirmation_url': self.request.build_absolute_uri(
                        new_user.get_activation_url()
                    )
                }
            )
        except:
            return render(
                request=self.request,
                template_name='account/send_email_failed.html'
            )

        return render(
            request=self.request,
            template_name='account/registration_successful.html'
        )


class ResetPasswordRequestView(RedirectAuthenticatedUserMixin,SendMailMixin, View):
    model = User
    form_class = ResetPasswordForm
    template_name = 'account/registration/reset_password_request.html'

    email_template_name = 'account/email_templates/reset_password_email.html'
    subject = "Reset Password"

    def get(self, request):
        return render(
            request=request,
            template_name=self.template_name,
            context={
                'form': self.form_class()
            }
        )

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_invalid(self, form):
        return render(
            request=self.request,
            template_name=self.template_name,
            context={
                'form': form
            }
        )

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        user = self.get_user(email)
        try:

            self.send_mail(
                to=user.email,
                context={
                    'reset_url': self.request.build_absolute_uri(
                        user.get_reset_pasword_url()
                    )
                }
            )
        except:
            return render(
                request=self.request,
                template_name='account/send_email_failed.html'
            )

        self.render_reset_password_email_sent()

    def get_user(self, email):
        try:
            return self.model.objects.get(
                email__iexact=email
            )
        except self.model.DoesNotExist:
            """
            If the user does not exist, we do not want to reveal this information to potential attackers.
            Instead, we show the user the same page as if the email address existed.
            This is a security measure to prevent attackers from guessing which email addresses are valid.
            """

            self.render_reset_password_email_sent()

        except self.model.MultipleObjectsReturned:
            pass

    def render_reset_password_email_sent(self):
        return render(
            request=self.request,
            template_name='account/registration/reset_password_email_sent.html'
        )


class ResetPasswordConfirmView(RedirectAuthenticatedUserMixin ,View):
    form_class = SetPasswordForm
    model = User
    template_name = 'account/registration/reset_password_confirmation.html'
    success_template_name = 'account/reset_password_successful.html'

    def get(self, request, activation_code, **kwargs):
        user = self.get_user()
        form = self.form_class(user=user)
        return render(
            request=request,
            template_name=self.template_name,
            context={
                'form': form
            }

        )

    def post(self, request, activation_code, **kwargs):
        user = self.get_user()
        form = self.form_class(user=user, data=request.POST)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        user = form.save(commit=False)  # it sets new password for user and returns user instance
        """ Just to make sure that if a user failed to activate account,
                this is available as another way"""
        user.is_active = True
        """Change the activation_code to prevent user to reuse the link again"""
        user.activation_code = get_random_string(72)
        user.save()
        return render(
            request=self.request,
            template_name=self.success_template_name,
        )
    def form_invalid(self, form):
        return render(
            request=self.request,
            template_name=self.template_name,
            context={
                'form': form
            }
        )

    def get_user(self):
        activation_code = self.kwargs.get('activation_code')
        try:
            return self.model.objects.get(
                activation_code__iexact=activation_code
            )

        except self.model.DoesNotExist:
            raise Http404


class ActivationView(RedirectAuthenticatedUserMixin ,View):
    model = User

    def get(self, request, activation_code, **kwargs):
        user = self.get_user()
        user.is_active = True
        user.activation_code = get_random_string(72)
        user.save()
        return render(
            request=request ,
            template_name='account/activation_successful.html',
        )

    def get_user(self):
        activation_code = self.kwargs.get('activation_code')
        try:
            return self.model.objects.get(
                activation_code__iexact=activation_code
            )

        except self.model.DoesNotExist:
            raise Http404