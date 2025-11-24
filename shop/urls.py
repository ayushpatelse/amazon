from django.urls import path,include
from . import views
urlpatterns = [
    path("",views.home,name="home"),
    path("signin/",views.signin,name="signin"),
    path("signout/",views.logout_user,name="signout"),
    path("signup/",views.signup,name="signup"),
    path("cart/",views.cart,name="cart"),
    path("View/<str:id>",views.View,name="view"),
    path("checkout/",views.checkout,name="checkout"),
    path("profile/",views.userProfile,name="profile"),
    path("updateCart/<str:method>",views.updateCart,name="updatecart"),
    path("processorder/",views.processOrder,name="processorder"),
    path("billing/",views.billing,name="billing"),
    

]
