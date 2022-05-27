# meli

Requisitos:
pip install Django
pip install redis
pip install requests
pip insttall celery

Install Redis on Linux:
https://redis.io/docs/getting-started/installation/install-redis-on-linux/


Levantar servicio Redis:
sudo service redis-server start

Celery:
https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html

Inicializar celery:
celery -A meli_proxy worker -l INFO

Proxy demo para challenge Mercado Libre

-- Crear redireccionar llamadas 
Se limita las consultas por IP a 10000 rpm por defecto

Configurar URL para conexion proxy, por ejemplo:
curl -i -H "Content-Type: application/json" -X POST -d '{"url":"https://api.mercadolibre.com/"}' http://localhost:8000/setUrl

Añadir limites de rpm a un path, por ejemplo:
curl -i -H "Content-Type: application/json" -X POST -d '{"path":"/categories/MLAASDS", "limit": 50000}' http://localhost:8000/limitar


Consulta a endpoint ejemplo:
curl http://localhost:3000/categories/MLAASDS
