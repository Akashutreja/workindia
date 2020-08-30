from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Note(models.Model):
  text = models.TextField(default='', blank=True)
  active  = models.BooleanField(default=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  created_at=models.DateTimeField(auto_now=False,auto_now_add=True,blank=False,null=False)
  last_modified=models.DateTimeField(auto_now=True,auto_now_add=False)
