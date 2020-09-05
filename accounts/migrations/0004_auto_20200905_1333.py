# Generated by Django 3.1 on 2020-09-05 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20200905_1333'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attrib',
            name='items',
        ),
        migrations.AddField(
            model_name='attrib',
            name='items',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.item'),
        ),
    ]
