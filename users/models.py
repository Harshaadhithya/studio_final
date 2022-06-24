import datetime
from statistics import mode
from tokenize import blank_re
from unicodedata import name
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


def year_choices():
    return [(r,r) for r in range(2012,datetime.date.today().year)]

class Profile(models.Model):
    role_choices=(
        ('admin','admin'),
        ('photographer','photographer'),
        ('normal_user','normal_user')
    )
    dept_choices=[
        ('ISE','ISE'),
        ('CSE','CSE'),
        ('ME','ME')
    ]
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=60)
    role=models.CharField(max_length=60,choices=role_choices,default='normal_user')
    roll_no=models.CharField(max_length=20,unique=True,null=True,blank=True)
    dept=models.CharField(max_length=60,choices=dept_choices,null=True,blank=True)
    batch=models.IntegerField(null=True,blank=True,choices=year_choices())
    mobile=models.IntegerField(null=True)
    verified=models.BooleanField(null=True,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    profile_img=models.ImageField(null=True,blank=True,upload_to='profile_imgs/')

    def __str__(self):
        if self.roll_no != '':
            return '{}-{}'.format(self.name,self.roll_no)
        else:
            return self.name



