from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import *
from django.db.models.signals import post_save
class SignUp(models.Model):
    username=models.CharField(max_length=200)
    email=models.CharField(max_length=254)
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    phoneno=models.CharField(max_length=200)
    address=models.CharField(max_length=450)
    password=models.CharField(max_length=250)
    utype=models.CharField(max_length=250)
    
class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    usernames=models.CharField(max_length=200)
    phoneno=models.CharField(max_length=200)
    address=models.CharField(max_length=450)
    utype=models.CharField(max_length=250)
    def __str__(self):  # __str__
        return (self.user.username)

class Newsletter(models.Model):
    email=models.CharField(max_length=300)

class Contact(models.Model):
    name=models.CharField(max_length=250)
    email=models.CharField(max_length=254)
    sub=models.CharField(max_length=1000)
    msg=models.CharField(max_length=1500)

class Store(models.Model):
    name=models.CharField(max_length=300)
    category=models.CharField(max_length=300)
    price=models.IntegerField()

class Transaction(models.Model):
    name=models.CharField(max_length=254)
    category=models.CharField(max_length=300)
    price=models.IntegerField()
    quantity=models.IntegerField()
    datetime=models.CharField(max_length=300)

class Advertisements(models.Model):
    header = models.CharField(max_length=255)
    text = models.CharField(max_length=1000)
    startdate = models.CharField(max_length=255)
    enddate = models.CharField(max_length=255)
    createdate = models.CharField(max_length=255)

class Emailsystem(models.Model):
    email=models.CharField(max_length=200)
    sub=models.CharField(max_length=500)
    msg=models.CharField(max_length=1000)
    time=models.CharField(max_length=150)
class CartData(models.Model):
    uname=models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    price = models.IntegerField()
    quantity = models.IntegerField()

class Trackorder(models.Model):
    uname=models.CharField(max_length=200)
    name=models.CharField(max_length=200)
    category=models.CharField(max_length=200)
    add=models.CharField(max_length=400)
    phone=models.EmailField(max_length=254)
    email=models.CharField(max_length=200)
    price=models.IntegerField()
    quantity=models.IntegerField()
    datetime=models.CharField(max_length=200)

class Demo(models.Model):
    demo1=models.CharField(max_length=200)
    demo2=models.CharField(max_length=200)