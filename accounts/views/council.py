from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from ..forms import CouncilForm
from ..models import Council, Item
from .tools import create_access_token

import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings


@login_required(login_url='login')
def council(request):
    items = Council.objects.filter(is_council=True).values('item__name', 'item__media')
    TEMPLATE_NAME = 'accounts/council.html'
    if 'add_council' in request.POST:
        item_name = request.POST.get('item')
        media = request.POST.get('media')

        try:
            item_from_bdd = Item.objects.get(name=item_name)
        except Item.DoesNotExist:
            item_from_bdd = None
            item_from_bdd = Item(name=item_name, media=media)
            item_from_bdd.save()

        try:
            item_is_council = Council.objects.get(item__name=item_name)
            if item_is_council:
                messages.warning(request, "L'item est déjà présent dans le loot council")
        except Council.DoesNotExist:
            item_is_council = None
            c = Council(item=item_from_bdd, is_council=True)
            c.save()

    if 'looking_for_item' in request.POST :
        item_name = request.POST.get('item_name')
        if item_name:
            token = create_access_token(settings.CLIENT_ID, settings.CLIENT_SECRET)
            token = token['access_token']
            r = requests.get(f'{settings.API_URL}{item_name}{settings.TOKEN_URL}{token}', params=request.GET)

            if r.status_code == 200: 
                data = r.json()
                datas = data['results']
                context = {'datas': datas, 'item_name': item_name, 'items': items}

                return render(request, TEMPLATE_NAME, context)
            else:
                messages.warning(request, "Merci de vérifier l'ortographe de l'item")
                context = {'items': items}
                return render(request, TEMPLATE_NAME, context)

    context = {'items': items}
    return render(request, TEMPLATE_NAME, context)