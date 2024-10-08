"""Models for the app Django application """
from django.db import models
# from django.db.models.constraints import UniqueConstraint

# Create your models here.
class MenuItem(models.Model):
    """ Defining a MenuItem model with the following fields """
    name= models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category =models.ManyToManyField('Category', related_name='item')
    
    def __str__(self):
        """ Defining a str model with the following fields """
        return self.name
        
    
class Category(models.Model):
    """ Defining a Category model with the following fields """
    name= models.CharField(max_length=100)
    
    def __str__(self):
        """ Defining a str model with the following fields """
        return self.name
        
class OrderModel(models.Model):
    """ Defining a Order model with the following fields """
    created_on = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=7,decimal_places=2)
    items = models.ManyToManyField('MenuItem', related_name='order', blank=True)
    
    name = models.CharField(max_length=50,blank=True)
    email = models.CharField(max_length=50,blank=True)
    street = models.CharField(max_length=50,blank=True)
    city = models.CharField(max_length=50,blank=True)
    state = models.CharField(max_length=15,blank=True)
    zip_code = models.IntegerField(blank=True, null= True)
    
    def __str__(self):
        """ Defining a str model with the following fields """
        return f'Order: {self.created_on.strftime("%b %d %I: %M %p")}'
        
