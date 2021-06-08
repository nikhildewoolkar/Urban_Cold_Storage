from django.contrib import admin
from .models import SignUp,UserProfile,Newsletter,Contact,Transaction,Advertisements,Emailsystem,Store
from .models import CartData,Trackorder
# Register your models here.
admin.site.register(SignUp)
admin.site.register(UserProfile)
admin.site.register(Newsletter)
admin.site.register(Contact)
admin.site.register(Transaction)
admin.site.register(Advertisements)
admin.site.register(Emailsystem)
admin.site.register(Store)
admin.site.register(CartData)
admin.site.register(Trackorder)