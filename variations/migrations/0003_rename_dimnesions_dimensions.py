# Generated by Django 3.2.16 on 2022-11-22 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0021_product_dimensions'),
        ('variations', '0002_dimnesions'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Dimnesions',
            new_name='Dimensions',
        ),
    ]
