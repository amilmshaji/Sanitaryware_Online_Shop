# Generated by Django 4.1.3 on 2023-05-11 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_alter_orderplaced_ordered_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderplaced',
            options={'verbose_name': 'Order Details', 'verbose_name_plural': 'Order Details'},
        ),
    ]