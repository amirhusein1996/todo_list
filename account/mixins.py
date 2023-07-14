from typing import Optional
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.mail import EmailMultiAlternatives
from django.core.validators import EmailValidator
from django.shortcuts import redirect
from django.template.loader import render_to_string

email_validator = EmailValidator()


class SendMailMixin:
    subject = None
    email_template_name = None
    to = None
    from_email = None

    def send_mail(
            self,
            subject=None,
            context=None,
            email_template_name=None,
            to=None,
            from_email: Optional[str] = None
    ):

        if subject is None:
            if hasattr(self, 'subject') and getattr(self, 'subject') is not None:
                subject = self.subject
            else:
                raise ImproperlyConfigured(
                    "Subject is required"
                )

        if context is None or not isinstance(context, dict):
            raise ImproperlyConfigured(
                "Context is required and must be a dictionary"
            )

        if email_template_name is None:
            if hasattr(self, 'email_template_name') and getattr(self, 'email_template_name') is not None:
                email_template_name = self.email_template_name
            elif hasattr(settings, 'DEFAULT_EMAIL_TEMPLATE_NAME'):
                email_template_name = settings.DEFAULT_EMAIL_TEMPLATE_NAME
            else:
                raise ImproperlyConfigured(
                    "No email template name provided and no default template name found in settings or class"
                )

        if to is None:
            if hasattr(self, 'to') and getattr(self, 'to') is not None:
                to = self.to
            else:
                raise ImproperlyConfigured(
                    "Recipient email is required"
                )
        else:
            try:
                email_validator(to)  # if no error raises , email is okay
            except ValidationError:
                raise ImproperlyConfigured(
                    "Invalid recipient email address"
                )

        if from_email is None:
            if hasattr(self, 'from_email') and getattr(self, 'from_email') is not None:
                from_email = self.from_email
        else:
            try:
                email_validator(from_email)
            except ValidationError:
                raise ImproperlyConfigured(
                    "Invalid sender email address"
                )

        html_body = render_to_string(template_name=email_template_name, context=context)
        email = EmailMultiAlternatives(subject=subject, body=html_body, to=[to],
                                       from_email=from_email or settings.DEFAULT_FROM_EMAIL)
        email.attach_alternative(html_body, 'text/html')
        email.send()


class RedirectAuthenticatedUserMixin:
    redirect_url = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_redirect_url())
        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self):
        if self.redirect_url:
            return self.redirect_url
        if hasattr(settings, 'LOGIN_REDIRECT_URL') and getattr(settings, 'LOGIN_REDIRECT_URL'):
            return getattr(settings, 'LOGIN_REDIRECT_URL')

        raise ImproperlyConfigured(
            "Failed to extract Redirect URL"
        )
