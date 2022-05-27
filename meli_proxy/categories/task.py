from celery.decorators import task
from .models import Connections
from .utils import insertConn

@task(name="add_conn_history")
def addConn(path, ip, date):
    insertConn(path, ip, date)

