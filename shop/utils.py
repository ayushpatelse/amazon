from django.shortcuts import redirect,render
from .models import *
import time
from django.core import serializers
from itertools import chain
from django.db.models import Q
def filter_web(crti:list[str]):
    all_data = {}
    

    
    for item in crti:
        
        list1 = []
        filter_item = Product.objects.values(item)
        for i in filter_item:
            a = i[item]
            if a not in list1:
                list1.append(a)
        all_data[item]=list1

        
        
    return all_data 

def multiQuery(data):
    prod = []
    for i in range(len(data)):
        q = Product.objects.filter(Q(brand__icontains=data[i]) & Q(price__icontains=data[i][:-2]))
        # print("====================",q)
        prod= list(chain(prod,q))

    return prod

def updateCart(request,method):
    num  = request.GET.get("fun")
    page = str(request.GET.get("page_url"))
    
    if request.user.is_authenticated :
        customer = request.user.customer
        # print("User :" ,customer)
        product = Product.objects.get(id = num)
        order ,created= Order.objects.get_or_create(customer=customer,complete=False)

        print("Order :" ,order,"Product :",product,"customer",customer)
        # print(product)     
        cartitem , created = CartItem.objects.get_or_create(order=order,product=product)
        print(cartitem)
        if method == "add" and product.stock>0 :
            cartitem.quantity = (cartitem.quantity + 1)   
        elif method == "remove" :
            cartitem.quantity = (cartitem.quantity - 1)

        if cartitem.quantity <=0:
            cartitem.delete()
        else:
            cartitem.save()
    else:
        print("Unauth user")
    if page == "2":
        return redirect("checkout")
    elif page == "1":
        return redirect("cart")
    else:
        return redirect("home")
    

