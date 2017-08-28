from django.shortcuts import render,render_to_response,HttpResponse,redirect
from django.conf import settings
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Question,Response
import random
from datetime import datetime,timedelta
import time
class QuestionDetailView(DetailView):
    model = Question
    template_name = "question_detail.html"
    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)

        #Randomly shuffles the options.
        response = Response.objects.get_or_create(user=self.request.user)
        response = response[0]
        context["options"]=response.get_options(int(self.kwargs['pk']))
        if datetime.combine(datetime.today(),response.start_time) + timedelta(minutes = settings.LEVEL1_TIME_LIMIT) > datetime.now():
            context["valid"]=True
            context["bookmarked"]=response.get_bookmarked_questions()
            context["answered"]=response.get_answered_questions()
        else:
            context["valid"]=False
        return context

def test(request):
    response = Response.objects.get_or_create(user=request.user)
    response=response[0]
    if datetime.combine(datetime.today(),response.start_time) + timedelta(minutes = settings.LEVEL1_TIME_LIMIT) > datetime.now():
        seq = response.get_sequence()
        questions=[]
        q=Question.objects.all()
        for i in seq:
            questions.append(q.get(id=i))
        context={"valid":True}
        context['questions']=questions
        context['answered']=response.get_answered_questions()
        context['bookmarked']=response.get_bookmarked_questions()
    else:
        context={"valid":False}
    return render(request,'test.html',context)

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
    response = Response.objects.get_or_create(user=request.user)
    response = response[0]
    response.start_test()
    return redirect("/level1/test")
