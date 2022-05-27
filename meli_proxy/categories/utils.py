from unittest import result
from django.db.models import Count
from .models import Connections


def insertConn(path, ip, date):
    conn = Connections()
    conn.created_at = date
    conn.path = path
    conn.ip_address = ip
    
    conn.save()
    

def estadistica(data):
    result = {}
    
    connection = Connections.objects.all()
    paths = connection.values('path').distinct()
 
    pathsDict  = {}
    
    for p in paths:
        if p['path'] not in pathsDict:
            pathsDict[p['path']] = 1
        else:
            pathsDict[p['path']] += 1
        
    ip_address = connection.values('ip_address').distinct()
    ipDict  = {}
    
    for ip in ip_address:
        if ip['ip_address'] not in ipDict:
            ipDict[ip['ip_address']] = 1
        else:
            ipDict[ip['ip_address']] += 1
    
    resumen = []
    resumen.append({'consultas_por_path':pathsDict})
    resumen.append({'consultas_por_ip':ipDict})
    
    result['estadisticas'] = resumen
    
    return result