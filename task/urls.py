from django.urls import path
from .views import *

app_name = "task"


base_urls = [
    path('',TodoListView.as_view() , name = 'task_view'),
]


ajax_urls = [
    path('ajax/todo-items/' , TodoListView.as_view() , name='ajax_todo_items'),
    path('ajax/todo-items/search/', TodoListView.as_view(), name='ajax_search_items'),
    path('ajax/item/delete/', ItemDeleteView.as_view() , name='ajax_delete_item'),
    path('ajax/item/create/' , ItemCreateView.as_view() , name='ajax_create_item'),
    path('ajax/item/upadte/<int:id>' , ItemUpdateView.as_view() , name='ajax_update_item'),
    path('ajax/item/update/progress/' , update_progress , name='ajax_update_progress'),


]


urlpatterns = base_urls + ajax_urls

