from django.db import models

# Create your models here.
class Module(models.Model):
    code = models.CharField(max_length = 10)
    rating = models.FloatField(default = 0.0)
    comment1 = models.CharField(max_length = 200, default = "")
    comment2 = models.CharField(max_length = 200, default = "")
    comment3 = models.CharField(max_length = 200, default = "")
    searched = models.IntegerField(default = 1)
    emotions = models.CharField(max_length = 200, default = "1.0,1.0,1.0,1.0,1.0")

class Issue(models.Model):
    code = models.CharField(max_length = 10, default = "")
    message = models.CharField(max_length=200, default = "")