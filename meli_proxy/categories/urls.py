# -*- coding: utf-8 -*-
from django.conf.urls import url

from categories.views import  proxyViews

urlpatterns = [
    url(r'^(?P<metodo>.*)/(?P<metodo_id>.*)$' , proxyViews)
    
]
