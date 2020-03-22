from django.urls import path, include

from .views import index, signup, logout_view, todo, todos

urlpatterns = [
    path('', index, name='index'),
    path('signup/', signup, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('todo/', todos, name='todos'),
    path('todo/<int:todo_id>/', todo, name='todo')
]

app_name = 'app'