from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

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
    query=request.GET['q']
    username=get_user_data(query)
    user = User.objects.get_or_create(username=query, password=username,first_name=username)
    login(request, user[0])
    return render(request,'profile.html',context={'username':username})


def home(request):
    return render(request,'home.html',{})