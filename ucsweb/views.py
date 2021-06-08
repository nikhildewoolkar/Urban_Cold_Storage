from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ObjectDoesNotExist
import datetime
import os
from django.conf import settings 
from django.core.mail import send_mail 
import numpy as np
from django.contrib import messages
from subprocess import check_output, CalledProcessError,STDOUT
from django.contrib.auth.models import User, auth
from django.http import HttpResponse, request
from .models import SignUp,UserProfile,Newsletter,Contact,Transaction,Advertisements,Emailsystem,Store
from .models import CartData,Trackorder,Transaction
def home(request):
    return render(request,"home.html")

def about(request):
    return render(request,"about.html")
def contact(request):
    if request.method=='POST':
        g=0
        name=request.POST.get("name")
        email=request.POST.get("email")
        subject=request.POST.get("subject")
        message=request.POST.get("message")
        c=Contact(name=name,email=email,sub=subject,msg=message)
        c.save()
        try:
            subject = 'Query/Suggestion Received'   
            message = f'Hi{name}--{email},Your response is received by Urban Cold Storage.We will reply as soon as possible.'
            email_from = settings.EMAIL_HOST_USER 
            recipient_list = [email] 
            send_mail( subject, message, email_from, recipient_list ,fail_silently=False)
            messages.info(request,'Query/Feedback Submitted.we will reply you soon.')
        except:
            messages.info(request,'Query/Feedback Submitted.we will reply you soon.')
        return render(request,"contact.html",{"g":g})
    return render(request,"contact.html")
def advertisement(request):
    w = reversed(Advertisements.objects.all())
    return render(request,"advertisement.html",{'w':w})
def signuplogin(request):
    return render(request,"signuplogin.html")
def signup(request):
    if request.method=='POST':
        first_name=request.POST.get("fname")
        last_name=request.POST.get("lname")
        username = request.POST.get("uid")
        phoneno=request.POST.get("phoneno")
        add= request.POST.get("add")
        email=request.POST.get("email")
        password=request.POST.get("pass")
        password1=request.POST.get("pass1")
        utype="normal"
        def password_check(password):
            SpecialSym =['$', '@', '#', '%'] 
            val = True
            if len(password) < 8:
                print('length should be at least 6') 
                val = False
            if len(password) > 20: 
                print('length should be not be greater than 8') 
                val = False
            if not any(char.isdigit() for char in password): 
                print('Password should have at least one numeral') 
                val = False
            if not any(char.isupper() for char in password): 
                print('Password should have at least one uppercase letter') 
                val = False
            if not any(char.islower() for char in password): 
                print('Password should have at least one lowercase letter') 
                val = False
            if not any(char in SpecialSym for char in password): 
                print('Password should have at least one of the symbols $@#') 
                val = False
            if val == False: 
                val=True
                return val                   
        if password==password1:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username taken')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'email taken')
                return redirect('signup')
            elif (password_check(password)):
                messages.info(request,'password is not valid')
                return redirect('signup')
            else:
                user=User.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name)
                user.save()
                work=SignUp(username=username,password=password,email=email,first_name=first_name,last_name=last_name,phoneno=phoneno,address=add,utype=utype)
                work.save()
                messages.info(request,"user created succesfully")
                user=auth.authenticate(username=username,password=password)
                if user is not None:
                   auth.login(request,user)
                u = User.objects.get(username=username)
                reg=UserProfile(user=u,usernames=username,phoneno=phoneno,address=add,utype=utype)
                reg.save()
                auth.logout(request)
        else:
            messages.info(request,"password not matching")
            return redirect('signup')
        return redirect('login')
    return render(request,"signup.html")
def login(request):
    if request.method=="POST":
        username=request.POST.get("email")
        password=request.POST.get("pwd")
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            p1=request.user
            d=UserProfile.objects.get(usernames=p1.username)
            if(d.utype=="normal"):
                return redirect('/')
            else:
                return render(request,"adminhome.html")
        else:
            messages.info(request,"Invalid Credentials")
            return redirect('login')
    return render(request,"login.html")
    return render(request,"login.html")
def logout(request):
    auth.logout(request)
    return render(request,"login.html")
def profile(request):
    p1=request.user
    id=""
    n=reversed(Trackorder.objects.filter(uname=p1.username))
    if request.method=="POST":
        id=int(request.POST.get("id"))
        print(id)
        return render(request,"profile.html",{"id":id,'n':n})
    return render(request,"profile.html",{"id":id,'n':n})
def editprofile(request):
    p=request.user
    if request.method=="POST":
        id=2
        fname=request.POST.get("fname")
        lname=request.POST.get("lname")
        uname=request.POST.get("username")
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        add=request.POST.get("add")    
        User.objects.filter(username=uname).update(first_name=fname,last_name=lname)
        UserProfile.objects.filter(usernames=uname).update(phoneno=phone,address=add)
        SignUp.objects.filter(username=uname).update(first_name=fname,last_name=lname,phoneno=phone,address=add)
        return render(request,"profile.html",{"id":id})
    id=2
    return render(request,"profile.html",{"id":id})
def changepassword(request):
    id=3
    if request.method == 'POST':
        old=request.POST.get("old")
        new1=request.POST.get("new1")
        new2=request.POST.get("new2")
        def passwordcheck(password):
            SpecialSym =['$', '@', '#', '%'] 
            val = True
            if len(password) < 8:
                print('length should be at least 6') 
                val = False
            if len(password) > 20: 
                print('length should be not be greater than 20') 
                val = False
            if not any(char.isdigit() for char in password): 
                print('Password should have at least one numeral') 
                val = False
            if not any(char.isupper() for char in password): 
                print('Password should have at least one uppercase letter') 
                val = False
            if not any(char.islower() for char in password): 
                print('Password should have at least one lowercase letter') 
                val = False
            if not any(char in SpecialSym for char in password): 
                print('Password should have at least one of the symbols $@#') 
                val = False
            return val
        p=request.user
        u1 = SignUp.objects.get(username=p.username)
        if(u1.password==old):
            if(new1==new2):
                password=new1
                if(passwordcheck(password)==True):
                    u = User.objects.get(username=p.username)
                    u.set_password(new1)
                    u.save()
                    SignUp.objects.filter(username=p.username).update(password=new1)
                    messages.info(request,"password Changed succesfully.Login using new Password.")
                    return redirect('logout')
                else:
                    messages.info(request,"Password should contain(0-9,a-z,A-Z,@)")
                    id=3
                    return render(request,"profile.html",{"id":id})    
            else:
                messages.info(request,"Password Don't Match")
                id=3
                return render(request,"profile.html",{"id":id})
        else:
            messages.info(request,"Old Password is not Correct or error occured.")
            id=3
            return render(request,"profile.html",{"id":id})
    id=3
    return render(request,"profile.html",{"id":id})
def forgotpassword(request):
    if request.method == 'POST':
        fname=request.POST.get("fname")
        lname=request.POST.get("lname")
        username=request.POST.get("uname")
        email=request.POST.get("email")
        phoneno=request.POST.get("phoneno")
        u=1
        try:
            pa=SignUp.objects.get(username=username)
        except:
            u=0
        if(u==1):
            password=pa.password
            if(fname == pa.first_name and lname == pa.last_name and phoneno ==pa.phoneno and email==pa.email):
                try:
                    subject = 'Forget Password(Resend)'   
                    message = f'Hi {pa.username},your password for the Urban Cold Storage is {password}. try logging in once again and change the password.'
                    email_from = settings.EMAIL_HOST_USER 
                    recipient_list = [pa.email] 
                    send_mail( subject, message, email_from, recipient_list ,fail_silently=False)
                    messages.info(request,"password has been sent to your registered email address,kindly check.")
                    return render(request,"login.html")
                except:
                    messages.info(request,"sorry for inconvenience.email sending fail. kindly send query on conact page with proper subject and text.we will contact you soon..")
                    return render(request,"login.html")
            else:
                messages.info(request,"Entered incorrect information.Try using correct credentials.")
            return render(request,"forgotpassword.html")
        else:
            messages.info(request,"User is not registered.kindly go to signup page and register.")
            return render(request,"login.html")
        return render(request,"login.html")
    return render(request,"forgotpassword.html")
def store(request):
    v=Store.objects.all()
    return render(request,"store.html",{'v':v})
def cart(request):
    p1=request.user
    username=p1.username
    v=CartData.objects.filter(uname=username)
    j=CartData.objects.filter(uname=username)
    total=0
    for j in j:
        total+=(j.price*j.quantity)
    return render(request,"cart.html",{'v':v,"total":total})
def newsletter(request):
    if request.method=="POST":
        g=1
        email=request.POST.get("email")
        d=Newsletter.objects.all()
        for d in d:
            if(email == d.email):
                messages.info(request,"Email already present in Newsletter database.")
                break
        else:
            wo=Newsletter(email=email)
            wo.save()
            try:
                subject = 'Newsletter Activated'   
                message = f'Hi {email},Newsletter Activated for your entered email address.Now you will get all the updates from Urban Cold Storage.'
                email_from = settings.EMAIL_HOST_USER 
                recipient_list = [email] 
                send_mail( subject, message, email_from, recipient_list ,fail_silently=False)
                messages.info(request,"Newsletter Activated.")
            except:
                messages.info(request,"Newsletter Activated.")
        return render(request,"contact.html",{"g":g})   
    return render(request,"contact.html")
    return render(request,"contactus.html")
def adminhome(request):
    return render(request,"adminhome.html")
def trackdetails(request):
    if request.method == 'POST':
        id=int(request.POST.get("id"))
        if(id == 1):
            m=reversed(Newsletter.objects.all())
        elif(id == 0):
            return render(request,"trackdetails.html")        
        elif(id == 0):
            return render(request,"trackdetails.html")        
        elif(id == 2):
            m=reversed(Contact.objects.all())
        else:
            m=User.objects.all()
        return render(request,"trackdetails.html",{"id":id,'m':m})
    return render(request,"trackdetails.html")
def trackorders(request):
    v=reversed(Trackorder.objects.all())
    return render(request,"trackorders.html",{'v':v})
def editstore(request):
    x = datetime.datetime.now()
    id=0
    n=Store.objects.all()
    now=x.strftime("%Y")+"-"+x.strftime("%m")+"-"+x.strftime("%d")
    if request.method=="POST":
        id=int(request.POST.get("id"))
        return render(request,"editstore.html",{"id":id,"now":now,'n':n})
    return render(request,"editstore.html",{"id":id,"now":now,'n':n})
def editadv(request):
    x = datetime.datetime.now()
    id=0
    n=Advertisements.objects.all()
    now=x.strftime("%Y")+"-"+x.strftime("%m")+"-"+x.strftime("%d")
    if request.method=="POST":
        id=int(request.POST.get("id"))
        return render(request,"editadv.html",{"id":id,"now":now,'n':n})
    return render(request,"editadv.html",{"id":id,"now":now,'n':n})
def addadv(request):
    id=1
    n=Advertisements.objects.all()
    x=datetime.datetime.now()
    now=x.strftime("%Y")+"-"+x.strftime("%m")+"-"+x.strftime("%d")
    if request.method=="POST":
        header=request.POST.get("head")
        text=request.POST.get("msg")
        startdate=request.POST.get("sdate")
        enddate=request.POST.get("edate")
        createdate=request.POST.get("cdate")
        action="AdvertisementAdded"
        if(Advertisements.objects.filter(header=header).exists()):
            messages.info(request,'Header Exists')
            return render(request,"editadv.html",{"id":id,"now":now,'n':n})
        else:
            t=Advertisements(header=header,text=text,startdate=startdate,enddate=enddate,createdate=createdate)
            t.save()
            messages.info(request,'Advertisement Added')
            return render(request,"editadv.html",{"id":id,"now":now,'n':n})
    return render(request,"editadv.html",{"id":id,"now":now,'n':n})
def deladv(request):
    x = datetime.datetime.now()
    id=2
    n=Advertisements.objects.all()
    now=x.strftime("%Y")+"-"+x.strftime("%m")+"-"+x.strftime("%d")
    if request.method=="POST":
        header=request.POST.get("id")
        g=Advertisements.objects.get(header=header)
        Advertisements.objects.filter(header=header).delete()
        return render(request,"editadv.html",{"id":id,"now":now,'n':n})   
    return render(request,"editadv.html",{"id":id,"now":now,'n':n})
def addstore(request):
    id=1
    n=Store.objects.all()
    x=datetime.datetime.now()
    now=x.strftime("%Y")+"-"+x.strftime("%m")+"-"+x.strftime("%d")
    if request.method=="POST":
        name=request.POST.get("name")
        category=request.POST.get("cat")
        price=request.POST.get("price")
        action="AdvertisementAdded"
        if(Store.objects.filter(name=name).exists()):
            messages.info(request,'Item Exists')
            return render(request,"editstore.html",{"id":id,"now":now,'n':n})
        else:
            t=Store(name=name,category=category,price=price)
            t.save()
            messages.info(request,'Item Added')
            return render(request,"editstore.html",{"id":id,"now":now,'n':n})
    return render(request,"editstore.html",{"id":id,"now":now,'n':n})
def delstore(request):
    x = datetime.datetime.now()
    id=2
    n=Store.objects.all()
    now=x.strftime("%Y")+"-"+x.strftime("%m")+"-"+x.strftime("%d")
    if request.method=="POST":
        name=request.POST.get("id")
        g=Store.objects.get(name=name)
        Store.objects.filter(name=name).delete()
        return render(request,"editstore.html",{"id":id,"now":now,'n':n})   
    return render(request,"editstore.html",{"id":id,"now":now,'n':n})
def emailsystem(request):
    m=reversed(Emailsystem.objects.all())
    id=0
    if request.method == 'POST':
        id=int(request.POST.get("id"))
        return render(request,"emailsystem.html",{"id":id,'m':m})
    return render(request,"emailsystem.html",{"id":id,'m':m})
def personalemail(request):
    id=2
    if request.method == 'POST':
        email=request.POST.get("email")
        sub=request.POST.get("sub")
        msg=request.POST.get("msg")
        time=datetime.datetime.now()
        s=Emailsystem(email=email,sub=sub,msg=msg,time=time)
        s.save()
        try:
            subject = sub   
            message = msg
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email] 
            send_mail( subject, message, email_from, recipient_list ,fail_silently=False)
            messages.info(request,"Personal mail sent Succesfully.")
        except:
            messages.info(request,"Personal mail Failed.")
        return render(request,"emailsystem.html",{"id":id})
    return render(request,"emailsystem.html",{"id":id})
def broadcastemail(request):
    id=3
    if request.method == 'POST':
        email="Broadcast email sent"
        sub=request.POST.get("sub")
        msg=request.POST.get("msg")
        time=datetime.datetime.now()
        k=Emailsystem(email=email,sub=sub,msg=msg,time=time)
        k.save()
        f=User.objects.all()
        g=[]
        for f in f:
            g.append(f.email)
        g1=Newsletter.objects.all()
        for g1 in g1:
            g.append(g1.email)
        e=list(set(g))
        try:
            subject = sub   
            message = msg
            email_from = settings.EMAIL_HOST_USER 
            recipient_list = e
            send_mail( subject, message, email_from, recipient_list ,fail_silently=False)
            messages.info(request,"broadcast mail sent Succesfully.")
        except:
            messages.info(request,"broadcast mail Failed.")
        return render(request,"emailsystem.html",{"id":id})
    return render(request,"emailsystem.html",{"id":id})

def checkout(request):
    if request.method=="POST":     
        g=int(request.POST.get("id"))
        return render(request,"checkout.html",{"g":g})
    return render(request,"checkout.html")

def addcart(request):
    v=Store.objects.all()
    p1=request.user
    if request.method=="POST":
        name=request.POST.get("name")
        category=request.POST.get("category")
        price=int(request.POST.get("price"))
        quantity=1
        uname=p1.username
        f=CartData(name=name,category=category,price=price,quantity=quantity,uname=uname)
        f.save()
        return render(request,"store.html",{'v':v})
    return render(request,"store.html",{'v':v})
def delcart(request):
    p1=request.user
    username=p1.username
    v=CartData.objects.filter(uname=username)
    j=CartData.objects.filter(uname=username)
    total=0
    for j in j:
        total+=(j.price*j.quantity)
    if request.method=="POST":
        if 'delete' in request.POST:    
            name=request.POST.get("name")
            category=request.POST.get("category")
            price=request.POST.get("price")
            cname=p1.username
            k=CartData.objects.filter(name=name,category=category).delete()
            v=CartData.objects.filter(uname=cname)
            j=CartData.objects.filter(uname=cname)
            total=0
            for j in j:
                total+=(j.price*j.quantity)
            return render(request,"cart.html",{'v':v,"total":total})
        if 'update' in request.POST:
            p1==request.user
            name=request.POST.get("name")
            category=request.POST.get("category")
            price=request.POST.get("price")
            cname=p1.username
            quantity=int(request.POST.get("quantity"))
            if(quantity == 0):
                quantity=1
            CartData.objects.filter(name=name,category=category).update(quantity=quantity)
            v=CartData.objects.filter(uname=cname)
            j=CartData.objects.filter(uname=cname)
            total=0
            for j in j:
                total+=(j.price*j.quantity)
            return render(request,"cart.html",{'v':v,"total":total})
    return render(request,"cart.html",{'v':v,"total":total})

def order(request):
    p1=request.user
    cname=p1.username
    if request.method=="POST":
        fname=request.POST.get("fname")
        lname=request.POST.get("lname")
        uname=request.POST.get("username")
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        add=request.POST.get("add")
        x = datetime.datetime.now()
        g=1
        k=[]
        b=CartData.objects.filter(uname=cname)
        for i in b:
            Trackorder(uname=uname,name=i.name,add=add,phone=phone,email=email,price=i.price,category=i.category,quantity=i.quantity, datetime=x).save()
        subject = 'Order Successfully Placed'
        message = f'Hi {p1.username}, thank you for Ordering.we will deliver the order within 30 mins.'
        email_from = settings.EMAIL_HOST_USER 
        recipient_list = [p1.email] 
        send_mail( subject, message, email_from, recipient_list ,fail_silently=False) 
        h=[]
        fh=SignUp.objects.filter(utype="admin")
        for i in fh:
            h.append(i.email)
        subject = 'Order Successfully Placed'
        message = f'Hi ,{fname} {lname} ({uname}), phone No.:-{phone},Email:-{email},Address:-{add} have ordered Meat from your Shop.kindly check client order details from tou transaction track manage portal and deliver the order within 30 mins.thank you.'
        email_from = settings.EMAIL_HOST_USER 
        recipient_list = h 
        print(recipient_list)
        send_mail( subject, message, email_from, recipient_list,fail_silently=False ) 
        b=CartData.objects.filter(uname=uname)
        b.delete()
        messages.info(request,'Order Placed')
        return render(request,"store.html",{"g":g})
    return render(request,"checkout.html")