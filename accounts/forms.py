from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from .models import *

class MemberForm(ModelForm):
    class Meta:
        model = Member
        fields = '__all__'
        exclude = ['user', 'grade']


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class WishlistForm(forms.ModelForm):
    order = forms.CharField(required=False)

    class Meta:
        model = Wishlist
        fields= '__all__'
        exclude = ['member']
    
class CouncilForm(ModelForm):
    class Meta:
        model = Council
        fields= '__all__'