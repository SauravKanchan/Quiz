from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import random

# Create your models here.

class Question(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    right_answer = models.CharField(max_length=500)
    wrong_answer_1 = models.CharField(max_length=500)
    wrong_answer_2 = models.CharField(max_length=500)
    wrong_answer_3 = models.CharField(max_length=500)
    right_answer_counts = models.PositiveIntegerField(default=0)
    wrong_answer_counts = models.PositiveIntegerField(default=0)

    def get_percentage_righ(self):
        return (self.right_answer_counts*100)/(self.right_answer_counts+self.wrong_answer_counts)

    def __str__(self):
        return self.title

class Response(models.Model):
    questions = Question.objects.all()
    random.shuffle(questions)
    questions = questions[:settings.NUMBER_OF_QUESTIONS]
    seq=""
    for i in questions:
        seq += str(i.id)+","
    try:
        if seq[-1]==",":seq=seq[:-1]
    except:
        pass

    user=models.OneToOneField(User)
    start_time = models.TimeField(null=True ,blank=True)
    answered_questions = models.CharField(max_length=200 ,blank=True)
    bookmarked_questions = models.CharField(max_length=200 ,blank=True)
    sequence = models.CharField(default=seq,max_length=200 ,blank=True)


    def get_answered_questions(self):
        a=self.answered_questions
        if len(a)>0:
            if a[0]!="{":
                a="{"+str(a)+"}"
            a=eval(a)
        else:
            a={}
        return list(map(int,a.keys()))

    def get_bookmarked_questions(self):
        if len(self.bookmarked_questions)>0:
            return list(map(int, self.bookmarked_questions.split(",")))
        return []
    def get_sequence(self):
        for i in range(100):print(self.sequence[0],len(self.sequence))
        if len(self.sequence)>0:
            return list(map(int, self.sequence.split(",")))

    def update_answered_questions(self,id,ans):
        """
        
        :param id: Question's Id that has to be added
        :param ans: answer given by user.
        :return: Updated dict of bookmarked_questions
        """
        a = self.get_answered_questions()
        if a[0]!="{":
            a="{"+a+"}"
        a=eval(a)
        a[id]=ans
        self.answered_questions = str(a)
        return a

    def update_bookmarked_questions(self, id):
        """

        :param id:Question's Id that has to be added /removed
        :return: Updated list of bookmarked_questions
        """
        a = self.get_bookmarked_questions()
        try:
            a.remove(id)
        except:
            a.append(id)
        self.bookmarked_questions = str(a)[1:-1]
        return a
    def __str__(self):
        return str(self.user)+" - response"