from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.db.models import Max, Count
from django.contrib.auth.decorators import login_required

# from ..filters import WishlistFilter
from ..decorators import allowed_users
from ..models import Wishlist, Member, Council, Item

import requests

API_URL = 'https://eu.api.blizzard.com/data/wow/search/item?namespace=static-eu&locale=fr_FR&name.en_US='
TOKEN_URL = '&orderby=name&_page=1&access_token=US4WGkPN65VVextZKtpwTS7jO70gsSVKWL'

@login_required(login_url='login')
def wishlist(request):
    user = request.user
    try:
        member_connected = Member.objects.get(email=user.email)
    except Member.DoesNotExist :
        member_connected = None
    

    wishlist_member = Wishlist.objects.filter(member=member_connected).values('order', 'item', 'item__name', 'item__media')
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
        item_name = request.POST.get('item')
        order = request.POST.get('order')
        media = request.POST.get('media')
        item_exist = Wishlist.objects.filter(member=member_connected, item__name=item_name)
        if order == "":
            messages.warning(request, "Merci de renseigner la position de l'item")
        elif order_max is not None and int(order) <= int(order_max):
            messages.warning(request, "Merci de choisir une position supérieur à la position de votre dernier item")
        elif item_exist:
            messages.warning(request, "L'item est déjà présent dans votre wishlist")
        elif Council.objects.filter(item__name=item_name, is_council=True).exists():
            messages.warning(request, "L'item est en loot council")
        else:
            messages.success(request, "Item ajouté à ta wishlist")
            try:
                item = Item.objects.get(name=item_name)
            except Item.DoesNotExist:
                item = None

            if item is None:
                item = Item(name=item_name, media=media)
                item.save()

            w = Wishlist(order=order, item=item, member=member_connected)
            w.save()
        
        context = {'wishlist_member': wishlist_member}
        return render(request, TEMPLATE_URL, context)
        
    context = {'wishlist_member': wishlist_member}
    return render(request, TEMPLATE_URL, context)

