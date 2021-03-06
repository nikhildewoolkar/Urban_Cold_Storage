from . import views
# from .views import *
from django.urls import path
urlpatterns=[
    path("",views.home,name="home"),
    path("home/",views.home,name="home"),
    path("about/",views.about,name="about"),
    path("signuplogin/",views.signuplogin,name="signuplogin"),
    path("signup/",views.signup,name="signup"),
    path("login/",views.login,name="login"),
    path("profile/",views.profile,name="profile"),
    path("editprofile/",views.editprofile,name="editprofile"),
    path("changepassword/",views.changepassword,name="changepassword"),
    path("forgotpassword/",views.forgotpassword,name="forgotpassword"),
    path("store/",views.store,name="store"),
    path("cart/",views.cart,name="cart"),
    path("contact/",views.contact,name="contact"),
    path("advertisement/",views.advertisement,name="advertisement"),
    path("logout/",views.logout,name="logout"),
    path("newsletter/",views.newsletter,name="newsletter"),
    path("adminhome/",views.adminhome,name="adminhome"),
    path("trackdetails/",views.trackdetails,name="trackdetails"),
    path("trackorders/",views.trackorders,name="trackorders"),
    path("editstore/",views.editstore,name="edittstore"),
    path("editadv/",views.editadv,name="editadv"),
    path("addadv/",views.addadv,name="addadv"),
    path("deladv/",views.deladv,name="deladv"),
    path("addstore/",views.addstore,name="addstore"),
    path("delstore/",views.delstore,name="delstore"),
    path("checkout/",views.checkout,name="checkout"),
    path("addcart/",views.addcart,name="addcart"),
    path("delcart/",views.delcart,name="delcart"),
    path("order/",views.order,name="order"),
    path("emailsystem/",views.emailsystem,name="emailsystem"),
    path("personalemail/",views.personalemail,name="personalemail"),
    path("broadcastemail/",views.broadcastemail,name="broadcastemail"),
]