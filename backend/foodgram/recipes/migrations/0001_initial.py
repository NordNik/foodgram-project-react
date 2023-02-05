# Generated by Django 4.0 on 2023-02-05 21:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('amount', models.DecimalField(decimal_places=1, max_digits=4)),
                ('slug', models.SlugField(unique=True)),
                ('units', models.TextField(max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Ingredients',
            },
        ),
        migrations.CreateModel(
            name='Recipes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, upload_to='recipes/', verbose_name='Photo')),
                ('text', models.TextField()),
                ('duration', models.DurationField(db_index=True, default=datetime.timedelta, verbose_name='Duration')),
            ],
            options={
                'verbose_name_plural': 'Recipes',
                'ordering': ['-duration'],
            },
        ),
    ]
