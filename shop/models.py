from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(blank=True,null=True,max_length=25)
    phone = models.PositiveIntegerField(blank=True,null=True)

    def __str__(self) :
        return self.user.username

class Catagory(models.Model):
    name = models.CharField(max_length=150,blank=False)
    def __str__(self):
        return self.name

class Product(models.Model):
    catagory = models.ForeignKey(Catagory,null=True,blank=False,on_delete=models.SET_NULL)
    pname = models.CharField(max_length=100,blank=False)
    brand = models.CharField(max_length=100,null=True,blank=False) 
    price = models.DecimalField(decimal_places=1,max_digits=10)
    desc = models.TextField(default="",blank=False)
    image = models.ImageField(upload_to="static/images")
    stock = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)


    def __str__(self):
       return self.pname
    
    @property
    def imageURL(self):
        try :
            url = self.image.url
        except :
            url =''
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer,null= True,blank=True,on_delete = models.SET_NULL)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=25)


    def __str__(self):
        return str(self.id)
    
    @property
    def get_total_items(self):
        cartitems = self.cartitem_set.all()
        total = sum([item.quantity for item in cartitems])
        # print(total)
        return total
    
    @property
    def get_total_price(self):
        cartitems = self.cartitem_set.all()
        total = sum([item.get_total for item in cartitems])
        # print(total)
        return total
    
    @property
    def addressUser(self):
        word = "working"
        address =  self.shippingdetail_set.all().first()
        
        # for 
        if address:
            word = address.address + "," + address.city + "," + address.state + "," + "India"
            print("address :",address)
        else:    
            word = "No selected address"


        return word 



class CartItem(models.Model):
    product = models.ForeignKey(Product,null=True,blank=True,on_delete=models.SET_NULL)
    order = models.ForeignKey(Order,null=True,blank=True,on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(default=0,null=True,blank=True)

    @property
    def get_total(self):
        total_price = self.product.price * self.quantity
        
        return total_price


class ShippingDetail(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    address = models.TextField(max_length=150)
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    pincode = models.CharField(max_length=150)
    

    def __str__(self):
        return str(self.customer) + "_" + str(self.order) + "_" + str(datetime.datetime.now().date())
    
    




    


     


