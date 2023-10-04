from django.contrib import admin
from .models import CustomUser, MyPassword

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(MyPassword)