# -*- coding: utf-8 -*-

from re import X
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

import requests
import json
import urllib.request as urllib2 

from django.http import StreamingHttpResponse
from .redis_utils import setValues, getValues, validRequestPath, validRequestIp

from .task import addConn
from .utils import estadistica

@csrf_exempt
def proxyViews(request, metodo, metodo_id):

    if metodo == 'limitar':
        return redirect('limitar')
    elif metodo == 'setUrl':
        return redirect('setUrl')
    elif metodo == 'estadisticas':
        return redirect('estadisticas')

    client_ip = request.META['REMOTE_ADDR']
    
    # Obtener servidor al que se conectara el proxy
    url_api = getValues('url')
    if url_api == None:
        return JsonResponse({'success':False, 'message':'Debe configurar URL'})
    
    url = str(url_api) + metodo + "/" + metodo_id
    
    now = datetime.now()
    path = "/" +  metodo + "/" + metodo_id
    
    # Validar limites de consultas por Path
    validReqByPath = validRequestPath(path, client_ip, now)
    if validReqByPath['success'] == False:
        return JsonResponse(validReqByPath)
    
    # Validar limites de consultas por IP
    validReqByIp = validRequestIp(path, client_ip, now)
    if validReqByIp['success'] == False:
        return JsonResponse(validReqByIp)
    
    addConn.delay(path, client_ip, now)
    response = requests.get(url, stream=True, headers={'user-agent': request.headers.get('user-agent')})
    return StreamingHttpResponse(
        response.raw,
        content_type=response.headers.get('content-type'),
        status=response.status_code,
        reason=response.reason)
    

@csrf_exempt
def limitarViews(request):
    if request.content_type == 'application/json':
        data = json.loads(request.body)
    else:
        data = request.POST

    if 'path' not in data or 'limit' not in data:
        return JsonResponse({'success':False, 'message':'No ha ingresado los parámetros necesarios'})
    
    if str(data['limit']).isdigit() == False or int(data['limit']) <= 0:
        return JsonResponse({'success':False, 'message':'limite debe ser entero mayor a cero'})
        
    setValues('limit-' + str(data['path']), data['limit'])
    return JsonResponse({'success': True, 'message':'se ha configurado limite para ' + str(data['path']) + ' exitosamente con valor ' + str(data['limit'])})


@csrf_exempt
def setPathViews(request):
    if request.content_type == 'application/json':
        data = json.loads(request.body)
    else:
        data = request.POST

    if 'url' not in data:
        return JsonResponse({'success':False, 'message':'No ha ingresado los parámetros necesarios'})

        
    setValues('url', str(data['url']))
    return JsonResponse({'success': True, 'message':'se ha configurado la url ' + str(data['url']) + ' exitosamente.'})

@csrf_exempt
def estadisticasViews(request):
    if request.content_type == 'application/json':
        data = json.loads(request.body)
    else:
        data = request.GET
    
    result = estadistica(data)
        
    return JsonResponse(result)
