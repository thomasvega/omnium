from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),


    path('account/', views.accountSettings, name="account"),
    path('wishlist/', views.wishlist, name="wishlist"),
]