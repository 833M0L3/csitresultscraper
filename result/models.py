from django.db import models

# Create your models here.

class Downloads(models.Model):
    key = models.CharField(primary_key=True,max_length=250)
    name = models.CharField(max_length=250)
    date = models.DateTimeField()
    link = models.CharField(max_length=250)
    def __str__(self):
        return self.name
    
class Students(models.Model):
    fname = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    symbol_num = models.IntegerField(primary_key=True)
    def __str__(self):
        return self.fname
    

class Results(models.Model):
    id = models.CharField(primary_key=True,max_length=250)
    key = models.CharField(max_length=250)
    symbol_num = models.IntegerField()
    date = models.DateTimeField()
    def __str__(self):
        return self.key
    

class Update(models.Model):
    id = models.CharField(primary_key=True,max_length=250)
    time = models.DateTimeField()
    def __str__(self):
        return self.time