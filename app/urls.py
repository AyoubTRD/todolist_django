from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import index, signup, logout_view, todo, todos

urlpatterns = [
    path('', index, name='index'),
    path('signup/', signup, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('todo/', todos, name='todos'),
    path('todo/<int:todo_id>/', todo, name='todo')
]

urlpatterns += staticfiles_urlpatterns()

app_name = 'app'