# -*- coding: utf-8 -*-
from django.conf.urls import url

from categories.views import  proxyViews, limitarViews, setPathViews, estadisticasViews


urlpatterns = [
    url(r'^(?P<metodo>.*)/(?P<metodo_id>.*)$' , proxyViews),
    url(r'limitar$' , limitarViews, name='limitar'),
    url(r'setUrl$' , setPathViews, name='setUrl'),
    url(r'estadisticas$' , estadisticasViews, name='estadisticas')
]
