# Generated by Django 3.2.16 on 2022-11-02 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0004_remove_reviewrating_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='created_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]