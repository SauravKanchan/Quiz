from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.conf import settings

from level1.models import Question

def profile(request):
    try:
        query=request.GET['q']
        username=request.GET['r']
        secret_key = request.GET['k']

        email = request.GET['e']

        if secret_key == "" and query!="":
            messages.add_message(request, messages.WARNING, 'Wrong Secret Key')
            return redirect("/")
        try:
            k = int(secret_key)
            q = int(query)
        except:
            k=1
            q=0
        if k==(q**3+2*q+10000)%(10009):
            if not username:
                messages.add_message(request, messages.WARNING , 'No such reciept exists.')
            try:
                user = User.objects.get_or_create(username=query,email=email, password=username,first_name=username)
            except:
                messages.add_message(request,messages.WARNING, 'Username and Reciept No do not match')
            login(request, user[0])
        else:
            messages.add_message(request, messages.WARNING, 'Wrong Secret Key')
            return redirect("/")
    except:
        username=request.user.first_name
    return render(request,'profile.html',context={'username':username,'completed':request.user.profile.completed_levels < 1})

def logout_view(request):
    logout(request)
    messages.add_message(request, messages.WARNING, settings.LOGOUT_MESSAGE)
    return redirect("/")

def home(request):
    return render(request,'home.html',{})