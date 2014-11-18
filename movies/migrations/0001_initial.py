# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('released', models.IntegerField()),
                ('restricted', models.IntegerField()),
                ('imdb', models.CharField(max_length=20)),
                ('image', models.URLField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Showtime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cinema', models.CharField(max_length=20)),
                ('time', models.CharField(max_length=20)),
                ('movie', models.ForeignKey(to='movies.Movie')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
