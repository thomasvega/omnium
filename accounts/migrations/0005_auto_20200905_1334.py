# Generated by Django 3.1 on 2020-09-05 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200905_1333'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attrib',
            old_name='items',
            new_name='item',
        ),
    ]
