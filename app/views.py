import json

from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.db import IntegrityError
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from app.models import Todo


def parse_body(body):
    return json.loads(body.decode('utf-8'))

def index(request):
    return render(request, 'registration/profile.html', {
        'title': 'Todo List App'
    })

def signup(request):
    message = ''
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            if not username:
                message = 'Please provide a correct username'
            elif len(password) < 5:
                message = 'The password can\'t be less than 5 characters'
            else:
                user = User.objects.create_user(username, password=password)
                user.save()
                user = authenticate(username=username, password=password)
                login(request, user)
                redirect(reverse('app:index'))

        except KeyError:
            message = 'Please fill in all the required fields'

        except IntegrityError:
            message = f'The username {request.POST["username"]} is already taken'

    return render(request, 'registration/signup.html', {
        'title': 'Sign up to our app', 'message': message
    })

def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html', {'title': 'Logged out successfully'})

@csrf_exempt
def todos(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'not authenticated'}, status=401)

    if request.method == 'POST':
        try:
            new_todo = parse_body(request.body)
            created_todo = request.user.todo_set.create(todo_text=new_todo['todo_text'])
            return JsonResponse(created_todo.as_dict(), status=201)
        except KeyError:
            return JsonResponse({'error': 'Please provide the todo'}, status=400)

    if request.method == 'GET':
        todos = [todo.as_dict() for todo in request.user.todo_set.order_by('-pub_date')]
        return JsonResponse(todos, safe=False)


@csrf_exempt
def todo(request, todo_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'not authenticated'}, status=401)

    if request.method == 'GET':
        try:
            todo = request.user.todo_set.get(id=todo_id)
            return JsonResponse(todo.as_dict())
        except Todo.DoesNotExist:
            return JsonResponse({'error': 'Todo not found'}, status=404)

    if request.method == 'PUT':
        try:
            todo = request.user.todo_set.get(id=todo_id)
            new_todo = parse_body(request.body)
            todo.is_done = new_todo.get('is_done') or todo.is_done
            todo.todo_text = new_todo.get('todo_text') or todo.todo_text

            todo.save()
            return JsonResponse(todo.as_dict())
        except Todo.DoesNotExist:
            return JsonResponse({'error': 'Todo not found'}, status=404)

    if request.method == 'DELETE':
        try:
            todo = request.user.todo_set.get(id=todo_id)
            todo.delete()
            return JsonResponse(todo.as_dict())
        except Todo.DoesNotExist:
            return JsonResponse({'error': 'Todo not found'}, status=404)