# -*- coding: utf-8 -*-
"""

@author: Saurav Kanchan

"""
from django.conf.urls import url,include
from .views import *

urlpatterns = [
    url(r'^$', test,name='test'),
    url(r'^response',add_response,name="add_response"),
    url(r'^question/(?P<pk>[-\w]+)/$', QuestionDetailView.as_view(), name='question-detail'),
]
