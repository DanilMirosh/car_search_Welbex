# Generated by Django 4.2.1 on 2023-05-26 18:31

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cargo_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='point',
            field=django.contrib.gis.db.models.fields.PointField(null=True, srid=4326),
        ),
    ]