# Generated by Django 3.1 on 2020-09-01 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200901_1043'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='grade',
            field=models.CharField(choices=[('Guild Master', 'Guild Master'), ('Officier', 'Officier'), ('Member', 'Member'), ('Pick Up', 'Pick Up')], max_length=12, null=True),
        ),
    ]
