from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages


def get_user_data(reciept_no):
    d={'12345':'Saurav',
       '11111': 'Kanchan',
       '99999': 'demo'}
    try:
        return d[reciept_no]
    except:
        return False
# Create your views here.
def profile(request):
    try:
        query=request.GET['q']
        username=get_user_data(query)
        if not username:
            messages.add_message(request, messages.INFO, 'No such reciept exists.')
            return redirect("/")
        user = User.objects.get_or_create(username=query, password=username,first_name=username)
        login(request, user[0])
    except:
        username=request.user.username
    return render(request,'profile.html',context={'username':username})

def logout_view(request):
    logout(request)
    return redirect("/")
def home(request):
    return render(request,'home.html',{})