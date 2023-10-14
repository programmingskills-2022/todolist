from django.shortcuts import render,redirect
from .models import Todo
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    user= request.user
    add=False
    if not user.is_authenticated:
        todolist=None
    else:
        q= request.GET.get('q') if request.GET.get('q') is not None else ''
        todolist= Todo.objects.filter((Q(title__icontains=q) | Q(description__icontains=q)) & (Q(user__username__icontains=request.user)))
    context={'add':add, 'todolist':todolist, 'user':user}
    return render(request, 'base/todo_list.html',context)

# User operations
def loginPage(request):
    page='login'
    user= None
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username= request.POST.get('username').lower()
        password= request.POST.get('password')
        try:
            user= User.objects.get(username=username)
        except:
            messages.error(request,'Username: %s is not exists'%username)

        user= authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, 'User:%s is not exists.'%username)
        else:
            login(request,user)
            return redirect('home')

    context={'page':page , 'user':user}
    return render(request, 'base/user_login.html',context)

def logoutPage(request):
    user=request.user
    if user.is_authenticated:
        logout(request)
        return redirect('home')
    context= {'user':user}
    return render(request, 'base/todo_list.html',context)

def registerPage(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'User information is invalid.')
    else:
        form = UserCreationForm()
    context= {'form':form}
    return render(request, 'base/user_register.html',context)

# todo crud operations
def deleteTodo(request,pk):
    todo= Todo.objects.get(id=pk)
    if request.method == 'POST':
        todo.delete()
        messages.info(request,f'{todo.title} has been deleted for {todo.user.username}.')
        return redirect('home')

    context={'obj':todo}
    return render(request, 'base/todo_delete.html',context)

def addTodo(request):
    todolist= Todo.objects.all()
    todo=None
    add=True
    title= request.POST.get('title')
    description= request.POST.get('description')
    if  request.POST.get('checked') is None:
        checked=False
    else:
        checked=True

    if request.method== 'POST':
        try:
            if title=='':
                raise Exception('Todo title is empty!')
            todo= Todo.objects.create(
                user= request.user,
                title=title,
                description=description,
                checked= checked
            )
            todo.save()
            messages.info(request,f'{todo.title} has been added for {todo.user.username}.' )
            return redirect('home')
        except Exception as error:
            messages.error(request,error)
    
    context={'add':add, 'todo':todo ,'todolist':todolist}
    return render(request, 'base/todo_list.html',context)

def editTodo(request,pk):
    add=True
    todolist= Todo.objects.all()
    todo= Todo.objects.get(id=pk)

    if request.method == 'POST':
        todo.title = request.POST.get('title')
        todo.description = request.POST.get('description')
        if request.POST.get('checked') is None:
            todo.checked=False    
        else:
            todo.checked = True

        todo.save()
        messages.info(request,f'{todo.title} has been updated for {todo.user.username}.')
        return redirect('home')

    context={'add':add, 'todo':todo ,'todolist':todolist}
    return render(request, 'base/todo_list.html',context)

def showTodo(request,pk):
    todo= Todo.objects.get(id=pk)
    context={'todo':todo}
    return render(request, 'base/todo_show.html',context)


