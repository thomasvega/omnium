# Generated by Django 3.1 on 2020-08-31 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_item_wishlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='item',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.DeleteModel(
            name='Item',
        ),
    ]
