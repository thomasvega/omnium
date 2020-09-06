from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from ..forms import CouncilForm
from ..models import Attrib, Item

@login_required(login_url='login')
def history(request):
    datas = Attrib.objects.filter().values('item__name', 'item__media', 'member__name', 'is_received', 'date')

    context = {'datas': datas}
    return render(request, 'accounts/history.html', context)