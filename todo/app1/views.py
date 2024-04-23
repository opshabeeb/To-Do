from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Userdetails,Project,Todo
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url="login")
def index(request):
    user = request.user
    if request.method == 'POST':
        pname = request.POST.get('pname')  
        if pname:  
            project = Project(title=pname, user=user) 
            project.save()
            return redirect('home')  

    projects = Project.objects.filter(user=user)
    return render(request, 'index.html', {'projects': projects})

def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    
    if request.method == 'POST':
        new_title = request.POST.get('edit_project_name')
        if new_title:
            project.title = new_title
            project.save()
    
    return redirect('home')

@login_required(login_url="login")
def todo(request,project_id):
    project = Project.objects.get(id=project_id)
    todos = project.todos.all()
    completed_todos = todos.filter(status='completed')
    pending_todos = todos.exclude(status='completed')
    
    context={
        'project':project,
        'todos':todos,
        'completed_todos': completed_todos,
        'pending_todos': pending_todos,
    }
    return render(request,'todo.html',context)

def add_todo(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        description = request.POST.get('description')
        if description:
            todoitem=Todo.objects.create(description=description,project=project)
            todoitem.save()
            return redirect('todo',project_id=project_id)
    else:
        return render(request,'todo.html')
    
def edit_todo(request,id):
    Data=Todo.objects.get(id=id)
    return render(request,'edit.html',{'Data':Data})
def update_todo(request,id):
    if request.method == 'POST':
       todo=Todo.objects.get(id=id)
       todo.description=request.POST.get('description')
       todo.save()
       project_id = todo.project.id
       return redirect('todo',project_id=project_id)
   
def delete_todo(request,id=id):
    item=Todo.objects.get(id=id)
    item.delete()
    project_id = item.project.id
    return redirect('todo',project_id=project_id)
 
def update_todo_status(request):
    if request.method == 'POST':
        todo_id = request.POST.get('todo_id')
        todo = get_object_or_404(Todo, pk=todo_id)
        todo.status = 'completed' if todo.status == 'pending' else 'pending'  # Toggle status
        print(todo.status)
        todo.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect('/')
    
def loginn(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            error_message = "invalid username or password"
            return render(request, 'registration/login.html', {'error_message': error_message})
    return render(request,'registration/login.html')

def signup(request):
    if request.method=='POST':
        ad=request.POST['address']
        phone=request.POST['phone']
        email=request.POST['email']
        fname=request.POST['firstname']
        lname=request.POST['lastname']
        username=request.POST['username']
        password=request.POST['password']
        password1=request.POST['confirm_password']
        
        if password != password1:
            error_message = "Passwords do not match."
            return render(request, 'registration/signup.html', {'error_message': error_message})
        
        # Check if email is already registered
        if User.objects.filter(email=email).exists():
            error_message = "This email is already registered."
            return render(request, 'registration/signup.html', {'error_message': error_message})
        
        # Check if username is already taken
        if User.objects.filter(username=username).exists():
            error_message = "This username is already taken."
            return render(request, 'registration/signup.html', {'error_message': error_message})
        
        user = User.objects.create_user(first_name=fname, last_name=lname, email=email, username=username, password=password)
        Userdetails.objects.create(user=user, address=ad, phone=phone)
        return redirect('login')
    return render(request,'registration/signup.html')

def logoutt(request):
    logout(request)
    return redirect('login')
