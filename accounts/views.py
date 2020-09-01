from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.forms import inlineformset_factory
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Count


from .forms import CreateUserForm, MemberForm, WishlistForm
from .decorators import allowed_users

import requests
from .models import *
# Create your views here.

def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for '+username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = { }
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    values = Wishlist.objects.filter().values('item', 'order', 'media', 'member', 'member__name', 'member__grade', 'member__class_played')
    print(values)
    context = {'values': values}
    return render(request, 'accounts/home.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['member', 'pu', 'officier', 'gm'])
def accountSettings(request):
    member = request.user.member
    form = MemberForm(instance=member)

    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
    
    context = {'form': form}
    return render(request, 'accounts/account_settings.html', context)


def wishlist(request):
    user = request.user
    user_id = user.id
    member_connected = Member.objects.get(id=user_id)
    wishlist_member = Wishlist.objects.filter(member=member_connected).values('item', 'media', 'order')
    if 'looking_for_item' in request.POST :
        item_name = request.POST.get('item_name')
        if item_name:
            r = requests.get(f'https://eu.api.blizzard.com/data/wow/search/item?namespace=static-eu&locale=fr_FR&name.en_US={item_name}&orderby=name&_page=1&access_token=US52YdGbvp6rGqTSF1JeRfGD18kYhLbp50', params=request.GET)

            if r.status_code == 200: 
                data = r.json()
                datas = data['results']
                context = {'datas': datas, 'item_name': item_name, 'wishlist_member': wishlist_member}

                return render(request, 'accounts/wishlist.html', context)
            else:
                messages.warning(request, "Merci de vérifier l'ortographe de l'item")
                context = {'wishlist_member': wishlist_member}
                return render(request, 'accounts/wishlist.html', context)
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
        else:
            messages.success(request, "Item ajouté à ta wishlist")
            w = Wishlist(order=request.POST.get('order'), item=request.POST.get('item'), media=request.POST.get('media'), member=member_connected)
            w.save()
        
        context = {'wishlist_member': wishlist_member}
        return render(request, 'accounts/wishlist.html', context)
    context = {'wishlist_member': wishlist_member}
    return render(request, 'accounts/wishlist.html', context)