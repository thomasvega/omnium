from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ..decorators import allowed_users
from ..forms import MemberForm

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

