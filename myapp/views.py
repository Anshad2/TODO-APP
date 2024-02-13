from django.shortcuts import render,redirect

from django.views.generic import View

from myapp.models import Task

from django import forms

from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout

from django.utils import timezone

from django.db.models import Sum

from django.utils.decorators import method_decorator

from django.contrib import messages

# Create your views here.


# decorators

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper
# task add view
# edit and upadte

class TaskForm(forms.ModelForm):
    class Meta:
        model=Task
        exclude=("created_date","user")
        widgets={
            "title":forms.TextInput(attrs={"class":"form-control"}),
            "description":forms.TextInput(attrs={"class":"form-control"}),
            "priority":forms.Select(attrs={"class":"form-control form-select"}),
            "completed":forms.CheckboxInput(attrs={"class":"form-check-input"}),            }
        



# registartion form
        
class RegistartionForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["username","email","password"]
        widgets={
            "username":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "password":forms.PasswordInput(attrs={"class":"form-control"})
        }

# login form
        
class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))

# view for creating task
    # url:localhost:8000/tasks/add/
    # method: get post
@method_decorator(signin_required,name="dispatch")
class TaskListView(View):
    def get(self,request,*args,**kwargs):
        qs=Task.objects.filter(user=request.user)
        return render(request,"task_list.html",{"data":qs})
    
@method_decorator(signin_required,name="dispatch")
class TaskCreateView(View):
    def get(self,request,*args,**kwargs):
        form=TaskForm()
        return render(request,"task_add.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=TaskForm(request.POST)
        if form.is_valid():
            # form.save()
            data=form.cleaned_data
            Task.objects.create(**data,user=request.user)
            messages.success(request,"Task has been addes successfully")

            return redirect("task-list")
        else:
            messages.error(request,"failed to add Task")
            return render(request,"task_add.html",{"form":form})
        
@method_decorator(signin_required,name="dispatch")
class TaskDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Task.objects.get(id=id)
        return render(request,"task_detail.html",{"data":qs})


# task delete view
    # url:localhost:8000/tasks/{id}/remove
@method_decorator(signin_required,name="dispatch")
class TaskDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Task.objects.filter(id=id).delete()
        return redirect("task-list")

# task update/edit view
    # url:localhost:8000/tasks/{id}/change/
@method_decorator(signin_required,name="dispatch")
class TaskEditView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        task_object=Task.objects.get(id=id)
        form=TaskForm(instance=task_object)
        return render(request,"task_edit.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        task_object=Task.objects.get(id=id)
        form=TaskForm(request.POST,instance=task_object)
        if form.is_valid():
            form.save()
            messages.success(request,"Task has been edited successfullu")
            return redirect("task-list")
        else:
            messages.error(request,"Task edut failed")
            return render(request,"task_edit.html",{"form":form})
        


# signup view
        
class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistartionForm()
        return render(request,"register.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=RegistartionForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            print("record has been added")
            return redirect("signin")
        else:
            print("failed")
            return render(request,"register.html",{"form":form})


# signin view
        
class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            u_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            print(u_name,pwd)
            user_object=authenticate(request,username=u_name,password=pwd)
            if user_object:
                print("valid")
                login(request,user_object)
                return redirect("task-list")
        print("invalid")
        return render(request,"login.html",{"form":form})
    
# signout view
@method_decorator(signin_required,name="dispatch")
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")