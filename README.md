# meli

Requisitos:
pip install Django
pip install redis
pip install requests


Proxy demo para challenge Mercado Libre

-- Crear redireccionar llamadas 
Se limita las consultas por IP a 10000 rpm por defecto

Configurar URL para conexion proxy, por ejemplo:
curl -i -H "Content-Type: application/json" -X POST -d '{"url":"https://api.mercadolibre.com/"}' http://localhost:8000/setUrl

Añadir limites de rpm a un path, por ejemplo:
curl -i -H "Content-Type: application/json" -X POST -d '{"path":"/categories/MLAASDS", "limit": 50000}' http://localhost:8000/limitar


Consulta a endpoint ejemplo:
curl http://localhost:8000/categories/MLAASDS

