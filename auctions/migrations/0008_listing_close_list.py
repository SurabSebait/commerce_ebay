# Generated by Django 4.2.2 on 2023-07-05 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='close_list',
            field=models.CharField(default='', max_length=3),
        ),
    ]
