from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Member)
admin.site.register(Wishlist)
admin.site.register(Council)