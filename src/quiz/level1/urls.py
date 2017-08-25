# -*- coding: utf-8 -*-
"""

@author: Saurav Kanchan

"""
from django.conf.urls import url,include
from .views import test,QuestionDetailView

urlpatterns = [
    url(r'^$', test,name='test'),
    url(r'^question/(?P<pk>[-\w]+)/$', QuestionDetailView.as_view(), name='question-detail'),
]
