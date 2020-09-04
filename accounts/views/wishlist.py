from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Max, Count

from ..filters import WishlistFilter
from ..decorators import allowed_users
from ..models import Wishlist, Member,Council

import requests

API_URL = 'https://eu.api.blizzard.com/data/wow/search/item?namespace=static-eu&locale=fr_FR&name.en_US='
TOKEN_URL = '&orderby=name&_page=1&access_token=USrhNEyDecSFzbHuhEb8pJfkDnNvb2fH0P'

def wishlist(request):
    user = request.user
    user_id = user.id
    member_connected = Member.objects.get(id=user_id)
    wishlist_member = Wishlist.objects.filter(member=member_connected).values('item', 'media', 'order')
    TEMPLATE_URL = 'accounts/wishlist.html'
    if 'looking_for_item' in request.POST :
        item_name = request.POST.get('item_name')
        if item_name:
            r = requests.get(f'{API_URL}{item_name}{TOKEN_URL}', params=request.GET)

            if r.status_code == 200: 
                data = r.json()
                datas = data['results']
                context = {'datas': datas, 'item_name': item_name, 'wishlist_member': wishlist_member}

                return render(request, TEMPLATE_URL, context)
            else:
                messages.warning(request, "Merci de vérifier l'ortographe de l'item")
                context = {'wishlist_member': wishlist_member}
                return render(request, TEMPLATE_URL, context)
    if 'add_wishlist' in request.POST:
        order_max = Wishlist.objects.filter(member=member_connected).aggregate(Max('order'))
        order_max = order_max['order__max']
        item_exist = Wishlist.objects.filter(member=member_connected, item=request.POST.get('item'))

        if request.POST.get('order') == "":
            messages.warning(request, "Merci de renseigner la position de l'item")
        elif order_max is not None and int(request.POST.get('order')) <= int(order_max):
            messages.warning(request, "Merci de choisir une position supérieur à la position de votre dernier item")
        elif item_exist:
            messages.warning(request, "L'item est déjà présent dans votre wishlist")
        elif Council.objects.filter(item=request.POST.get('item')).exists():
            messages.warning(request, "L'item est en loot council")
        else:
            messages.success(request, "Item ajouté à ta wishlist")
            w = Wishlist(order=request.POST.get('order'), item=request.POST.get('item'), media=request.POST.get('media'), member=member_connected)
            w.save()
        
        context = {'wishlist_member': wishlist_member}
        return render(request, TEMPLATE_URL, context)
    context = {'wishlist_member': wishlist_member}
    return render(request, TEMPLATE_URL, context)

