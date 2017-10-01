# -*- coding: utf-8 -*-
"""

@author: Saurav Kanchan

"""
from django.conf.urls import url,include
from .views import *

urlpatterns = [
    url(r'^$', start_test, name='start_test'),
    url(r'^endtest', end_test, name='end_test'),
    url(r'^test', test,name='level1'),
    url(r'^response',add_response,name="add_response"),
    url(r'^bookmark',bookmark,name="bookmark"),
    url(r'^question/(?P<pk>[-\w]+)/$', QuestionDetailView.as_view(), name='question-detail'),
]
