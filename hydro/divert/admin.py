from django.contrib import admin

# Register your models here.

from .models import GeoPoint 
#admin.site.register(User)
#admin.site.register(UserData)
admin.site.register(GeoPoint)
