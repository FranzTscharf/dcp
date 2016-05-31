# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-31 23:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dcp', '0011_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer_immaterial',
            name='location_x',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='offer_immaterial',
            name='location_y',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='offer_material',
            name='location_x',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='offer_material',
            name='location_y',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='search_immaterial',
            name='location_x',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='search_immaterial',
            name='location_y',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='search_material',
            name='location_x',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='search_material',
            name='location_y',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='offer_material',
            name='image',
            field=models.ImageField(upload_to='upload/'),
        ),
        migrations.AlterField(
            model_name='search_material',
            name='image',
            field=models.ImageField(upload_to='upload/'),
        ),
    ]