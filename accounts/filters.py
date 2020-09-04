import django_filters

from .models import Wishlist

# class WishlistFilter(django_filters.FilterSet):
#     class Meta:
#         model = Wishlist
#         fields = {
#             'item': [ 'contains'],
#             'member__class_played': ['exact']
#         }
#         exclude = ['order', 'media']