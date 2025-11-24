from math import ceil
from django.db.models import Q
from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import *
from .utils import *
import json
# Create your views here.

def home(request):
    # print(prod)
    # if data :
    #     print("entered")
    #     prod = multiQuery(data)

    if request.user.is_authenticated:
        customer = request.user.customer
        # print(customer)
        order ,created = Order.objects.get_or_create(customer=customer,complete =False)
    else:
        order = {"get_total_items":0,"get_total_price":0}
        if not request.COOKIES.get('GuestUserCart'):
            # Creates cokie if does not exist
            response = JsonResponse({"message": "Guest user cart created"})
            response.set_cookie('GuestUserCart',"$")
            return response
        else:
            cookie = request.COOKIES.get('GuestUserCart')
            if cookie !="$":
                cookie  = cookie.split("+")
                for d in cookie :
                    d = json.loads(d)
                    order['get_total_items'] += d['quantity']
            print(cookie)
            # print("No Cookie") 
           
    main = request.GET.get('mcat')
    maincat = Catagory.objects.all()
    search = request.GET.get('search') 

    if main :
        prod = Product.objects.filter(catagory__name=main)
    elif search :
        prod  = Product.objects.filter(Q(brand__icontains=search)|Q(pname__icontains=search))   
    else :
        prod  = Product.objects.all()

    
    
    jump = 4 
    allprod = []
    for i in range(0,len(prod),jump):
        
        allprod.append(prod[i:i+jump])
    crti = ["price","brand"]
    all_data = filter_web(crti)
    print("-------------------------------------------------")
    content = {
        "products":allprod ,    
        "order":order,
        "categories":maincat,
        "s_data" : all_data,
        
        }
    return render(request,"shop/home.html" , content)


def View(request,id):
    context = {"Product" : None,"categories" :None,"order":None}
    context['maincat'] = Catagory.objects.all()
    context['Product'] = Product.objects.get(id=id)
    if request.user.is_authenticated:
        customer = request.user.customer
        context['order'],created = Order.objects.get_or_create(customer=customer,complete =False)
        print(context)
        
    else:
        # Creates cookie if does not 
        context['order'] = {"get_total_items":0,"get_total_price":0}
        
        check = render(request,"shop/view.html",context)
        GuestData = None 
        check.set_cookie('GuestUserCart',GuestData)

    return render(request,"shop/view.html",context)

def cart(request):
    
    if request.user.is_authenticated:

        customer = request.user.customer
        
        order ,created = Order.objects.get_or_create(customer=customer,complete =False)
        items = order.cartitem_set.all()
    else:   
        items = []
        order = {"get_total_items":0,"get_total_price":0}
        cookie = request.COOKIES.get('GuestUserCart')
        if cookie !="$" and cookie is not None:
            cookie  = cookie.split("+")
            for d in cookie :
                print("+")
                d = json.loads(d)
                try  :
                    p = Product.objects.get(id=d["id"])
                    order["get_total_price"] += p.price
                    order['get_total_items'] += d['quantity']
                    item = {
                        'id':d["id"],
                        'product':{
                            
                            "pname":p.pname,
                            "brand":p.brand,
                            "price":p.price,
                            "desc":p.desc,
                            "image":p.imageURL,
                        },
                        "quantity":d["quantity"]
                    }

                    items.append(item)
                    print("item",items)
                except ValueError :
                    print()  

    context = {
        "items":items,
        "order":order,
    }
    return render(request,"shop/cart.html",context)


def checkout(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        
        order ,created = Order.objects.get_or_create(customer=customer,complete =False)
        
        items = order.cartitem_set.all()

    else: 
        items = []
        order = {"get_total_items":0,"get_total_price":0}
        cookie = request.COOKIES.get('GuestUserCart')
        if cookie !="$" and cookie is not None:
            cookie  = cookie.split("+")
            for d in cookie :
               
                d = json.loads(d)
                try  :
                    p = Product.objects.get(id=d["id"])
                    order["get_total_price"] += p.price
                    order['get_total_items'] += d['quantity']
                    item = {
                        'id':d["id"],
                        'product':{
                            
                            "pname":p.pname,
                            "brand":p.brand,
                            "price":p.price,
                            "desc":p.desc,
                            "image":{"url":p.imageURL},
                        },
                        "get_total":p.price * d["quantity"],
                        "quantity":d["quantity"],
                    }

                    items.append(item)
                except ValueError :
                    print("Data not found")

        # print(items)
        customer = {"name":"Username","email":"xyz@gmail.com"}
    
    context = {
        "data":customer,
        "items":items,
        "order":order,
    }
        
    return render(request,"shop/checkout.html",context)

def logout_user(request):
    logout(request)
    return redirect("home")
def signup(request):


    if request.method =="POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        
        
        if name  and email  and pass1 and pass2   :
            
            # Coolboy@2
            if pass1!=pass2 :
                return HttpResponse("Plz Write Same Password")
            else:
                try:
                    
                    my = User.objects.create(username=name,email=email,password=pass1)
                    # print(my)
                    customer = Customer.objects.create(user=my,phone=phone)
                    my.save()
                
                    return redirect('signin')
                except :
                    

                    return redirect('signin')
        else :
           return render(request,"shop/signup.html")
    return render(request,"shop/signup.html")

def signin(request):
    
    if request.method=="POST":
        uname = request.POST.get('name')
        pass1 = request.POST.get('pass')
        # print(uname,pass1)
        # kpatel@3014
      
        user = authenticate(request,username=uname,password=pass1)
        print("user :",user)
        if user is not None:
            login(request,user)
            messages.success(request,f"Logged in Successfully, {user} ")
            return redirect("home")
        else:
            return HttpResponse("Username or password is  incorrect ")
    return render(request,"shop/login.html")


def processOrder(request):
    data = json.loads(request.body)
    formData = data.get("PaymentForm")

    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        order.transaction_id = str(datetime.datetime.now())
        print("Order :",order,"Customer :",customer)
        shipping = ShippingDetail.objects.create(
            order=order,
            customer=customer,
            address= formData['address'],
            state = formData['state'],
            city = formData['city'],
            pincode=formData['pincode'],
        )
        order.complete = True
        order.save()
        shipping.save()
        print("Shipping Data Saved ok")
    else :
        return redirect('signup')
    
    return JsonResponse({"Form":"Submited"})

def userProfile(request):
    user = request.user
    print(user)
    data = Customer.objects.get(user=user)
    order = Order.objects.filter(customer=data)
    print(order)
    context = {"userData":data,"userOrder":order}
    return render(request,'shop/profile.html',context)

def billing(request):
    return render(request,'shop/billing.html')