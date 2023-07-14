from django.contrib.auth.decorators import login_required
from django.db.models.functions import Concat
from django.db.models import Value, CharField
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import ListView, DeleteView, CreateView, UpdateView
from django.urls import resolve
from django.views.decorators.http import require_POST

from .forms import TaskModelForm
from .models import Task


class TodoListView(ListView):
    context_object_name = 'tasks'
    model = Task
    paginate_orphans = 3
    paginate_by = 1
    ordering = ['-created_at', '-priority', '-deadline']

    def get_template_names(self):
        resolver_match = resolve(self.request.path_info)
        url_name = resolver_match.url_name

        if url_name == 'task_view':
            return 'task/todo.html'

        if url_name == 'ajax_todo_items' or url_name == "ajax_search_items":
            return 'task/components/_todo_items.html'

        return super().get_template_names()

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset.filter(user=self.request.user)

        """search query"""
        search_query = self.request.GET.get('search_query')
        if search_query:
            """
            This concatenates the title and description fields together with a space 
            in between, then filters the queryset to find icontains matches within 
            the concatenated search_td field.
            ///// search_td is stand for "search 'title' 'description'" /////
            An alternative approach is to use Q and the | operator to filter on 
            icontains matches in title and description separately. But this 
            concatenation allows matching the search term across the title
            and description in one filter.
            Note: it's not a search engine , just a simple search provided.
            """
            return queryset.annotate(
                search_td=Concat(
                    'title', Value(' '), 'description',
                    output_field=CharField()
                )
            ).filter(
                search_td__icontains=search_query
            )

        """filter by query params"""
        priority = self.request.GET.get('priority')
        progress = self.request.GET.get('progress')
        category = self.request.GET.get('category')
        if priority and priority != 'all':
            queryset = queryset.filter(priority=priority)
        if progress and progress != 'all':
            queryset = queryset.filter(progress=progress)
        if category and category != 'all':
            queryset = queryset.filter(category=category)

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'progress': self.model.Progress.choices,
            'priority': self.model.Priority.choices,
            'category': self.model.Category.choices,
        })

        return context

    def render_to_response(self, context, **response_kwargs):
        resolver_match = resolve(self.request.path_info)
        url_name = resolver_match.url_name

        if url_name == 'ajax_todo_items' or url_name == "ajax_search_items":
            html = render_to_string(template_name=self.get_template_names(), context=context)
            return JsonResponse(
                {
                    'data': html
                }
            )

        return super().render_to_response(context, **response_kwargs)


class ItemDeleteView(View):
    model = Task

    def post(self, request):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse(
            {
                'data': True
            }
        )

    def get_object(self):
        id = self.request.POST.get('id')
        return get_object_or_404(
            klass=self.model,
            pk=id,
            user=self.request.user
        )


class ItemCreateView(CreateView):
    form_class = TaskModelForm

    def form_valid(self, form):
        task = form.save(commit=False)
        task.user = self.request.user
        task.save()
        return JsonResponse(
            {
                'data': True
            }
        )

    def form_invalid(self, form):
        return JsonResponse(
            {
                'data': form.errors.as_json(),
            },
            status=400  # bad request
        )


class ItemUpdateView(UpdateView):
    model = Task
    form_class = TaskModelForm

    def get_object(self, queryset=None):
        id = self.kwargs.get('id')

        return get_object_or_404(
            klass=self.model,
            pk=id,
            user=self.request.user
        )

    def form_valid(self, form):
        form.save()
        return JsonResponse(
            {
                'data': True
            }
        )

    def form_invalid(self, form):
        return JsonResponse(
            {
                'data': form.errors.as_json(),
            },
            status=400  # bad request
        )


@require_POST
@login_required
def update_progress(request):
    try:
        task = Task.objects.get(
            pk=request.POST.get('id'),
            user=request.user
        )

        task.progress = request.POST.get('progress')
        task.save()
    except Task.DoesNotExist:
        raise Http404

    return JsonResponse(
        {
            'data': True
        }
    )
