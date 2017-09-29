from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.conf import settings


def get_user_data(reciept_no):
    d={'12345':'Saurav',
       '11111': 'Kanchan',
       '99999': 'demo',
       '22222':'neel',
       '66666':'lol',
       '00000':'superman',
       '20006':'shreya',
       '20000':'Yash',
       '10000':'Puthran',
       '30000':'Aditi',
       '40000':'batman',
       '50000':'hulk',
       '60000':'timepass',
       '33333':'Kunal'}
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
            messages.add_message(request, messages.WARNING , 'No such reciept exists.')
            return redirect("/")
        user = User.objects.get_or_create(username=query, password=username,first_name=username)
        login(request, user[0])
    except:
        username=request.user.first_name
    return render(request,'profile.html',context={'username':username,'completed':request.user.profile.completed_levels < 1})

def logout_view(request):
    logout(request)
    messages.add_message(request, messages.WARNING, settings.LOGOUT_MESSAGE)
    return redirect("/")
def home(request):
    return render(request,'home.html',{})