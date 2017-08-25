from django.shortcuts import render
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
    # seq = response.sequence

    return render(request,'question_detail.html',{})