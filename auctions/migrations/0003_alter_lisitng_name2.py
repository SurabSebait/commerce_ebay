# Generated by Django 4.2.2 on 2023-06-29 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_lisitng_name2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lisitng',
            name='name2',
            field=models.CharField(max_length=350),
        ),
    ]