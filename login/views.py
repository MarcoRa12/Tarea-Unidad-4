from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
# Create your views here.


def home(request):
    return render(request, "home.html")


def signup(request):

    if request.method == 'GET':
        print("Enviando datos")
        return render(request, "signup.html", {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # register user
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('task')
            except IntegrityError:

                return render(request, "signup.html", {
                    'form': UserCreationForm,
                    'error': "Usuario existe"
                })
        return render(request, "signup.html", {
            'form': UserCreationForm,
            'error': "Contraseña no coiciden "
        })


def task(request):
    tasks = Task.objects.filter(
        user=request.user, FechaCompletada__isnull=True)

    return render(request, 'task.html', {
        'tasks': tasks
    })


def cerrar(request):
    logout(request)
    return redirect('home')


def inicio_sesion(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        print(request.POST)
        user = authenticate(
             request, username=request.POST['username'], password=request.POST['password'])
        print(user)
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })


def created_task(request):

    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('task')
        except:
            return render(request, 'create_task.html', {
                'form': TaskForm, 'error': 'Ingrese datos validos'
            })
