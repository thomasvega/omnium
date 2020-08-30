from django.shortcuts import render

# Create your views here.

def registerPage(request):
    context = {}
    return render(request, 'accounts/register.html', context)


def loginPage(request):
    pass

def home(request):
    return render(request, 'accounts/home.html')