from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ..models import Wishlist
# from ..filters import WishlistFilter

@login_required(login_url='login')
def home(request):
    values = Wishlist.objects.filter().values('order', 'item__name', 'item__media', 'member', 'member__name', 'member__grade', 'member__class_played')
    print(values)
    # filterForm = WishlistFilter(request.GET, queryset=values)
    # list_users = filterForm.qs
    # if "filter_data" in request.GET:
    #     context = {'values': list_users, 'filterForm': filterForm}
    #     return render(request, 'accounts/home.html', context)

    # context = {'values': values, 'filterForm': filterForm}
    context = {'values': values, }
    return render(request, 'accounts/home.html', context)

