# Generated by Django 3.2.16 on 2023-02-25 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0022_product_display2'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='display3',
            field=models.ImageField(default='a3.png', upload_to='photos/display'),
        ),
    ]