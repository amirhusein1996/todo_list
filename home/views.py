from django.urls import reverse_lazy
from django.views.generic.base import TemplateView ,RedirectView
from django.shortcuts import reverse, redirect


class IndexTemplateView(TemplateView):
    template_name = 'home/index.html'

    def dispatch(self, request, *args, **kwargs):
        """
        logged in users are not allowed to see this page
        """
        if self.request.user.is_authenticated:
            return redirect(reverse('task:task_view'))
        return super().dispatch(request, *args, **kwargs)


class HomeOrTaskRedirectView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return reverse_lazy("task:task_view")
        return reverse_lazy('home:home_view')
