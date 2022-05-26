import imp
from urllib import response
from django.test import SimpleTestCase, Client
from django.urls import reverse
import json

# Create your tests here.
class proxyViews(SimpleTestCase):
    
    def test_categories(self):
        response = self.client.get('/categories/DEMO')
        content = json.loads(str(response.content , encoding='utf8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content['success'], False)
        
    
    def test_categoriesWithLimit(self):
        self.client.post('/limitar', data={'path':'/categories/TEST','limit':1000})
        response = self.client.get('/categories/TEST')
        
        content = json.loads(list(response.streaming_content)[0].decode("utf-8"))
        
        self.assertIn('message', content)
        self.assertIn('status', content)
        
    
        
    def test_limitar(self):
        response = self.client.post('/limitar', data={'path':'/categories/TEST','limit':1000})
        content = json.loads(str(response.content , encoding='utf8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content['success'], True)
        
        response = self.client.post('/limitar', data={'path':'/categories/TEST'})
        content = json.loads(str(response.content , encoding='utf8'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content['success'], False)
        self.assertEqual(content['message'],'No ha ingresado los parámetros necesarios')
        
    
    def test_estadisticas(self):
        response = self.client.get('/estadisticas?path=/categories/DEMO')
        content = json.loads(str(response.content , encoding='utf8'))
        path = content['path']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(path), 1)
        self.assertEqual(path[0]['cantidad'], 0)
        self.assertEqual(path[0]['path'], '/categories/DEMO')
        