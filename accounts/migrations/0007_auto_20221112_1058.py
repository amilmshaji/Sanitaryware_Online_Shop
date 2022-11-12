# Generated by Django 3.2.16 on 2022-11-12 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20221027_1956'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='address_line_1',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='address_line_2',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='country',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='profile_picture',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='fname',
            field=models.CharField(blank=True, editable=False, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='house',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='lname',
            field=models.CharField(blank=True, editable=False, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='phone_number',
            field=models.BigIntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='pin',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='street',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='city',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='state',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]