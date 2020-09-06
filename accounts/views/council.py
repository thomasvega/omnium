from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from ..forms import CouncilForm
from ..models import Council, Item

import requests
API_URL = 'https://eu.api.blizzard.com/data/wow/search/item?namespace=static-eu&locale=fr_FR&name.en_US='
TOKEN_URL = '&orderby=name&_page=1&access_token=USd4iFYTqnoakJt8T4Jono8vl28hDGoL1t'


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
            r = requests.get(f'{API_URL}{item_name}{TOKEN_URL}', params=request.GET)

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