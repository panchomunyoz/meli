import redis
import json

r = redis.Redis(host='localhost', port='6379',db=0 , charset="utf-8", decode_responses=True)

def setValues(key,value):
    r.set(key, value)

def getValues(key):
    return r.get(key)

def coutValuesByKey(key):
    values = {}
    resp = getValues(key)
    if resp != None:
        values = json.loads(resp)
        return len(values)
    return 0


def validRequestPath(path, client_ip, date):
    result = {'success':False, 'message':'Error desconocido'}

    limiteSolicitiud = getValues('limit-' + str(path))
    limiteSolicitiud = int(limiteSolicitiud) if limiteSolicitiud else 0

    if limiteSolicitiud == 0:
        return {'success':False, 'message':'No se ha definido el limite de solicitudes para ' + path}
        
    keySolicitud = path + '-' + date.strftime('%Y%m%d%H%M')

    solicitudes = coutValuesByKey(keySolicitud)
    
    data = []
    if solicitudes > 0:
                
        if  limiteSolicitiud < solicitudes:
            return {'success':False, 'message':'Se han sobrepasado los limites de consultas al path por minuto para ' + path}

        resp = getValues(keySolicitud)
        data = json.loads(resp)
        
    
    values = {'ip':client_ip,'date':date.strftime('%Y-%m-%d %H:%M:%S.%f')}
    data.append(values)

    setValues(keySolicitud,str(json.dumps(data)))
    saveReq(path, date)
    
    result['success'] = True
    result['message'] = 'Exito'
    return result


def validRequestIp(path, client_ip, date):
    result = {'success':False, 'message':'Error desconocido'}
    
    keyConsulta = str(client_ip) + '-' + date.strftime('%Y%m%d%H%M')
    consultas = coutValuesByKey(keyConsulta)
    
    # limitar consultas por IP
    if consultas == 0:
        setValues(client_ip, 10000)
        
    limiteConsulta = getValues('limit-' + str(client_ip))
    limiteConsulta = int(limiteConsulta) if limiteConsulta else 0
    
    if limiteConsulta > 0 and limiteConsulta < consultas:
        return {'success':False, 'message':'Se han sobrepasado los limites de consultas por minuto'}
    
    respConsulta = getValues(keyConsulta)
    dataConsulta = []
    
    if respConsulta: 
        dataConsulta = json.loads(respConsulta)
    
    dataConsulta.append({'path_destino':path, 'date':date.strftime('%Y-%m-%d %H:%M:%S.%f')})
 
    setValues(keyConsulta, str(json.dumps(dataConsulta)))
    saveReq(client_ip,date)
    
    result['success'] = True
    result['message'] = 'Exito'
    return result


def saveReq(key, date):
    data = getValues(key)
    data = json.loads(data) if data != None else []
    try:
        data.append({'date':date.strftime('%Y-%m-%d %H:%M:%S.%f')})
    except:
        data = []
        data.append({'date':date.strftime('%Y-%m-%d %H:%M:%S.%f')})
        
    setValues(key, str(json.dumps(data)))
