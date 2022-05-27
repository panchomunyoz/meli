from ipaddress import ip_address
from django.db import models
from datetime import datetime

class Connections(models.Model):
    created_at = models.DateTimeField()
    path = models.TextField(null=False, blank=False, db_index=True)
    ip_address = models.CharField(max_length=15, null=False, blank=False, db_index=True)
    
    def __unicode__(self):
        return str(self.id)
    
    class Meta:
        ordering = ('created_at',)