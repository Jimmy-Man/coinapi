from django.db import models

# Create your models here.

class domain(models.Model):
    domain_name     = models.CharField(max_length=120,default='')    
    domain_address  = models.CharField(max_length=120,default='')
    data_add        = models.IntegerField()

class api_token(models.Model):
    pass