# Generated by Django 3.2.16 on 2022-11-13 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20221113_1107'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderplaced',
            name='address_line_1',
        ),
        migrations.RemoveField(
            model_name='orderplaced',
            name='address_line_2',
        ),
        migrations.RemoveField(
            model_name='orderplaced',
            name='city',
        ),
        migrations.RemoveField(
            model_name='orderplaced',
            name='country',
        ),
        migrations.RemoveField(
            model_name='orderplaced',
            name='email',
        ),
        migrations.RemoveField(
            model_name='orderplaced',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='orderplaced',
            name='ip',
        ),
        migrations.RemoveField(
            model_name='orderplaced',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='orderplaced',
            name='order_note',
        ),
        migrations.RemoveField(
            model_name='orderplaced',
            name='order_number',
        ),
        migrations.RemoveField(
            model_name='orderplaced',
            name='order_total',
        ),
        migrations.RemoveField(
            model_name='orderplaced',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='orderplaced',
            name='state',
        ),
        migrations.RemoveField(
            model_name='orderplaced',
            name='tax',
        ),
    ]
