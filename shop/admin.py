from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Catagory)
admin.site.register(CartItem)
admin.site.register(ShippingDetail)
admin.site.register(Order)
