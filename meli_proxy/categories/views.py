# -*- coding: utf-8 -*-

from django.http import JsonResponse
import requests
import json
import urllib.request as urllib2 

from django.http import StreamingHttpResponse


def proxyViews(request, metodo, metodo_id):
    url = "https://api.mercadolibre.com/"+ metodo + "/" + metodo_id
    
    response = requests.get(url, stream=True, headers={'user-agent': request.headers.get('user-agent')})
    return StreamingHttpResponse(
        response.raw,
        content_type=response.headers.get('content-type'),
        status=response.status_code,
        reason=response.reason)