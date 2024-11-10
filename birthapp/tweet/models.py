from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.
class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=16)
    text = models.TextField(max_length=240)
    email = models.EmailField(default="example@gmail.com")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_of_birth = models.DateField(default=datetime.datetime.now().strftime("%Y-%m-%d"))
    email_status = models.CharField(max_length=20,default='ABC')

    def __str__(self):
        return f'{self.user.username} - {self.text[:10]}'
