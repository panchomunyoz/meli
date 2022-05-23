from django.db import models
from django.forms import DateTimeField

# Create your models here.
from django.utils import timezone


# almacena
class Connections(models.Model):
    ip_origin = models.CharField(max_length=15)
    path_destiny = models.CharField(max_length=255)
    last_connection = DateTimeField()
    
    def save(self, *args,**kwargs):
        self.last_connection = timezone.now()
        return super(Connections, self).save(*args,**kwargs)
