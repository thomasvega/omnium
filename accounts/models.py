from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class_played_choice = (

)

class Member(models.Model):
    class_played_choice = (
        ("Chaman", "Chaman"), 
        ("Chasseur", "Chasseur"),
        ("Démoniste", "Démoniste"),
        ("Druide", "Druide"),
        ("Guerrier", "Guerrier"),
        ("Mage", "Mage"),
        ("Prêtre", "Prêtre"),
        ("Voleur", "Voleur"),
    )
    member_grade = (
        ("Guild Master", "Guild Master"),
        ("Officier", "Officier"),
        ("Member", "Member"),
        ("Pick Up", "Pick Up"),
    )
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    class_played = models.CharField(choices=class_played_choice, max_length=10, null=True)
    grade = models.CharField(choices=member_grade, max_length=12, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=200, null=True)
    media = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Wishlist(models.Model):
    order = models.IntegerField(null=True)
    item = models.ForeignKey(Item, null=True, on_delete=models.SET_NULL)
    member = models.ForeignKey(Member, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.item.name


class Council(models.Model):
    item = models.ForeignKey(Item, null=True, on_delete=models.SET_NULL)
    is_council = models.BooleanField(null=True)

    def __str__(self):
        return self.item.name


class Attrib(models.Model):
    items = models.ManyToManyField(Item)
    members = models.ManyToManyField(Member)
    is_received = models.BooleanField(null=True)

    def __str__(self):
        return self.items.name