from django.db import models

# Create your models here.

class Login(models.Model):
    email=models.EmailField()
    password=models.CharField(max_length=30)
    role=models.CharField(max_length=20)


class Registration(models.Model):
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    role=models.CharField(max_length=50)
    login_id=models.OneToOneField(Login,on_delete=models.CASCADE,default=100)

class Category(models.Model):
    categoryname=models.CharField(max_length=50)
    categoryimage=models.URLField(max_length=200)

class Product(models.Model):
    productname=models.CharField(max_length=50)
    price=models.CharField(max_length=50)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    image=models.URLField(max_length=200)

class Review(models.Model):

    productid=models.CharField(max_length=50)
    userid=models.CharField(max_length=50)
    description=models.CharField(max_length=50)

class Cart(models.Model):
    productid=models.CharField(max_length=50)
    userid=models.CharField(max_length=50)
    quantity=models.CharField(max_length=50)
    productname=models.CharField(max_length=50)
    cartstatus=models.CharField(max_length=50)
    price=models.CharField(max_length=50)
    productid=models.CharField(max_length=50)
    image=models.URLField(max_length=250)

class Wishlist(models.Model):
    userid=models.CharField(max_length=50)
    productname=models.CharField(max_length=50)
    Wishliststatus=models.CharField(max_length=50,default=1)
    price=models.CharField(max_length=50)
    productid=models.CharField(max_length=50)
    image=models.ImageField(upload_to='images')
    
class Order(models.Model):
    userid=models.CharField(max_length=50)
    productname=models.CharField(max_length=50)
    orderstatus=models.IntegerField(default=1)
    price=models.CharField(max_length=50)
    productid=models.CharField(max_length=50)
    image=models.ImageField(upload_to='images')

class Address(models.Model):
    name=models.CharField(max_length=50)
    street=models.CharField(max_length=250)
    userid=models.OneToOneField(Login,on_delete=models.CASCADE)
    city=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    postal_code=models.CharField(max_length=100)







