from django.shortcuts import render, redirect
from django.contrib import messages

from ..forms import CouncilForm
from ..models import Council

import requests
API_URL = 'https://eu.api.blizzard.com/data/wow/search/item?namespace=static-eu&locale=fr_FR&name.en_US='
TOKEN_URL = '&orderby=name&_page=1&access_token=USrhNEyDecSFzbHuhEb8pJfkDnNvb2fH0P'

def council(request):
    items = Council.objects.all()
    council_form = CouncilForm()
    TEMPLATE_NAME = 'accounts/council.html'
    if 'add_council' in request.POST:
        print(request.POST.get('item'))
        try:
            item_exist = Council.objects.get(item=request.POST.get('item'))
        except Council.DoesNotExist:
            item_exist = None
        
        if item_exist:
            messages.warning(request, "L'item est déjà présent dans le loot council")
        else:
            c = Council(item=request.POST.get('item'), media=request.POST.get('media'))
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