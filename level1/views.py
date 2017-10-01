from django.shortcuts import render,render_to_response,HttpResponse,redirect
from django.conf import settings
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Question,Response
from django.contrib import messages
from django.contrib.auth.models import User
import operator
import random
from datetime import datetime,timedelta
import time
class QuestionDetailView(DetailView):
    model = Question
    template_name = "question_detail.html"
    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        response = Response.objects.get_or_create(user=self.request.user)
        response = response[0]
        context["options"]=response.get_options(int(self.kwargs['pk']))
        context['answered_option']=response.get_answer(int(self.kwargs['pk']))
        if not response.expired() and int(self.request.user.profile.completed_levels) < 1:
            context["valid"]=True
            context["bookmarked"]=response.get_bookmarked_questions()
            context["answered"]=response.get_answered_questions()
            context["time"]=response.get_expiry_time()
            ls=response.get_sequence()
            current_index = ls.index(int(self.kwargs['pk']))
            if len(ls)>current_index+1:
                context["next"]=ls[current_index+1]
            if current_index - 1>= 0:
                context["previous"] = ls[current_index - 1]

        else:
            context["valid"]=False
            return context
        return context

def test(request):
    if int(request.user.profile.completed_levels) < 1:
        response = Response.objects.get_or_create(user=request.user)
        response=response[0]
        if not response.expired():
            seq = response.get_sequence()
            questions=[]
            q=Question.objects.all()
            for i in seq:
                questions.append(q.get(id=i))
            context={'valid':True}
            context['questions']=questions
            context['answered']=response.get_answered_questions()
            context['bookmarked']=response.get_bookmarked_questions()
            context["time"] = response.get_expiry_time()
        else:
            return redirect("level1/endtest")
        return render(request,'test.html',context)
    else:
        messages.add_message(request, messages.INFO, 'You have already completed this test')
        return redirect("/profile")

def add_response(request):
    if request.method == "POST":
        question_id=request.POST["question_id"]
        ans = request.POST["ans"]
        resp = Response.objects.get_or_create(user=request.user)
        resp=resp[0]
        t=resp.update_answered_questions(int(question_id),ans)
    return render_to_response('question_detail.html',{})

def bookmark(request):
    if request.method == "POST":
        question_id=request.POST["question_id"]
        resp = Response.objects.get_or_create(user=request.user)
        resp=resp[0]
        resp.update_bookmarked_questions(int(question_id))
    return render_to_response('question_detail.html',{})

def start_test(request):
    if int(request.user.profile.completed_levels) < 1:
        response = Response.objects.get_or_create(user=request.user)
        response = response[0]
        response.start_test()
        return redirect("/level1/test")
    else:
        messages.add_message(request, messages.INFO, 'You have already completed this test')
        return redirect("/profile")

def end_test(request):
    request.user.profile.update_level(1)
    response = Response.objects.get_or_create(user=request.user)
    response = response[0]
    score = response.score()
    request.user.profile.update_points(score)
    l={}
    users = User.objects.all()
    for i in users:
        try:
            if int(i.profile.completed_levels)>=1:
                l[i.first_name]=i.profile.points
        except:pass
    leaderboard = sorted(l.items(), key=operator.itemgetter(1))
    leaderboard.reverse()
    return render(request,"end_test.html",{"score":score,"leaderboard":leaderboard})