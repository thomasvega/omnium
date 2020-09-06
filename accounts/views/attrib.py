from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from ..models import Item, Council, Member, Attrib
from ..forms import AttribForm

@login_required(login_url='login')
def attrib(request):
    attrib_form = AttribForm()
    members = Member.objects.all()
    items = Item.objects.all()

    if request.method == 'POST':
        member = request.POST.get('member')
        item = request.POST.get('item')
        if member and item:
            member = Member.objects.get(name=member)
            item = Item.objects.get(name=item)
            attrib_exist = Attrib.objects.filter(item=item, member=member, is_received=True)
            print(attrib_exist)
            if attrib_exist:
                messages.warning(request, 'Le joueur a déjà reçu cet item')
            else:
                messages.success(request, "L'attribution du joueur a bien été effectué")
                a = Attrib(member=member, item=item, is_received=True)
                a.save()

    context = {'attrib_form':attrib_form, 'members': members, 'items': items}
    return render(request, 'accounts/attrib.html', context)