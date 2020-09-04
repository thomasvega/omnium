from django.contrib import admin

# Register your models here.
from .models import Member, Wishlist, Council, Item, Attrib

admin.site.register(Member)
admin.site.register(Wishlist)
admin.site.register(Council)
admin.site.register(Item)
admin.site.register(Attrib)