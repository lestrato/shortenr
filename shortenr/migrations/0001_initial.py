# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-26 15:10
from __future__ import unicode_literals

import shortenr.fields.slug_field
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShortenedUrl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scheme', models.CharField(blank=True, max_length=10, null=True)),
                ('path', models.TextField()),
                ('query', models.TextField(null=True)),
                ('url_slug', shortenr.fields.slug_field.AutoSlugField(unique=True)),
                ('created_on', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShortenedUrlStat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device', models.CharField(blank=True, max_length=50, null=True)),
                ('browser', models.CharField(blank=True, max_length=50, null=True)),
                ('ip_address', models.CharField(blank=True, max_length=50, null=True)),
                ('viewed_on', models.DateField(auto_now_add=True)),
                ('url', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shortenr.ShortenedUrl')),
            ],
        ),
    ]
