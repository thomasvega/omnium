from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.forms import inlineformset_factory
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.db.models import Max


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
    members = Member.objects.all()
    member_group = request.user.groups.all()
    context = {'members': members}
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
    WishlistFormSet = inlineformset_factory(Member, Wishlist, fields=('order', 'item'))
    member_connected = Member.objects.get(id=user_id)
    print(WishlistFormSet)
    formset = WishlistFormSet(instance=member_connected)
    # if 'looking_for_item' in request.POST :
    #     item_name = request.POST.get('item_name')
    #     if item_name:
    #         r = requests.get(f'https://eu.api.blizzard.com/data/wow/search/item?namespace=static-eu&locale=fr_FR&name.en_US={item_name}&orderby=name&_page=1&access_token=USJY0wX2Hyql2ao82qh3qhKUiIQVkdunaf', params=request.GET)
    #         if r.status_code == 200: 
    #             data = r.json()
    #             datas = data['results']
    #             print(formset)
    #             context = {'datas': datas, 'item_name': item_name, 'formset': formset}

    #             return render(request, 'accounts/wishlist.html', context)
    #         else:
    #             context = {'error_message': "Merci de vérifier l'ortographe de l'item"}
    #             return render(request, 'accounts/wishlist.html', context)
    # if 'add_wishlist' in request.POST:
    #     form = WishlistFormSet(request.POST, instance=member_connected)
    #     if form.is_valid():
    #         form.save()


    context = {'formset': formset}
    return render(request, 'accounts/wishlist.html', context)