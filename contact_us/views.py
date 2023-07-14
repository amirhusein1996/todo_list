from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.generic import FormView
from .forms import ContactUsModelForm
from .models import ContactUsMessage


class ContactUsFormView(FormView):
    model = ContactUsMessage
    form_class = ContactUsModelForm
    template_name = 'contact_us/contact_us.html'
    success_url = '/'
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {
                'user':self.request.user
            }
        )
        return kwargs

    def form_valid(self, form):
        self.model.objects.create(
            user= self.request.user if self.request.user.is_authenticated else None,
            **form.cleaned_data
        )

        return JsonResponse(
            {
                'html':render_to_string(template_name='contact_us/message_received.html')
            }
        )

    def form_invalid(self, form):
        print(self.request.POST)
        return JsonResponse({
            'html': str(form.errors)
        },
        status=403
        )


