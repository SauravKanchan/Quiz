# -*- coding: utf-8 -*-
"""

@author: Saurav Kanchan

"""
from django.conf.urls import url,include
from .views import *

urlpatterns = [
    url(r'^$', home,name='home'),
    url(r'^profile/',profile,name='profile'),
    url(r'^level1/',include('level1.urls')),
    url(r'^logout/',logout_view,name="logout"),
]
