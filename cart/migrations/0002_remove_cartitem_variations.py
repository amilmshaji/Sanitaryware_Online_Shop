# Generated by Django 3.2.16 on 2023-03-07 03:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='variations',
        ),
    ]
