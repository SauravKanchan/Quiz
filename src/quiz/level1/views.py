from django.shortcuts import render,render_to_response,HttpResponse
from django.conf import settings
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Question,Response
import random

class QuestionDetailView(DetailView):
    model = Question
    template_name = "question_detail.html"
    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        context['options']=[context['object'].right_answer,context['object'].wrong_answer_1,context['object'].wrong_answer_2,context['object'].wrong_answer_3]
        #Randomly shuffles the options.
        random.shuffle(context['options'])
        return context

def test(request):
    response = Response.objects.get_or_create(user=request.user)
    response=response[0]
    seq = response.get_sequence()
    context={}
    questions = Question.objects.all().filter(id__in=seq)
    context['questions']=questions
    context['answered']=response.get_answered_questions()
    return render(request,'test.html',context)

def add_response(request):
    if request.method == "POST":
        question_id=request.POST["question_id"]
        ans = request.POST["ans"]
        resp = Response.objects.get_or_create(user=request.user)
        resp=resp[0]
        resp.update_answered_questions(int(question_id),ans)
        for i in range(100):print("response:- ",question_id,ans,request.POST)
    return render_to_response('question_detail.html',{})