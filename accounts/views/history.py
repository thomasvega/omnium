from django.shortcuts import render, redirect
from django.contrib import messages

from ..forms import CouncilForm
from ..models import Attrib, Item


def history(request):
    datas = Attrib.objects.filter().values('item__name', 'item__media', 'member__name', 'is_received', 'date')

    print(datas)

    context = {'datas': datas}
    return render(request, 'accounts/history.html', context)