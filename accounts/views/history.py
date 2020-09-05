from django.shortcuts import render, redirect
from django.contrib import messages

from ..forms import CouncilForm
from ..models import Council, Item


def history(request):
    context = {}
    return render(request, 'accounts/history.html', context)