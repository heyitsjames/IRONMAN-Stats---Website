# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('distance', models.CharField(choices=[('half-ironman', 'half-ironman'), ('full-ironman', 'full-ironman')], max_length=40)),
                ('title', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('location', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='RaceResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('athlete_name', models.CharField(max_length=255)),
                ('age_group', models.CharField(choices=[('Pro', 'Pro'), ('18-24', '18-24'), ('25-29', '25-29'), ('30-34', '30-34'), ('35-39', '35-39'), ('40-44', '40-44'), ('45-49', '45-49'), ('50-54', '50-54'), ('55-59', '55-59'), ('60-64', '60-64'), ('65-69', '65-69'), ('70-74', '70-74'), ('75-79', '75-79'), ('80-999', '80-999')], max_length=255)),
                ('sex', models.CharField(choices=[('M', 'M'), ('F', 'F')], max_length=1)),
                ('athlete_country', models.CharField(blank=True, null=True, max_length=255)),
                ('division_rank', models.IntegerField(blank=True, null=True)),
                ('gender_rank', models.IntegerField(blank=True, null=True)),
                ('overall_rank', models.IntegerField(blank=True, null=True)),
                ('swim_time', models.TimeField(blank=True, null=True)),
                ('bike_time', models.TimeField(blank=True, null=True)),
                ('run_time', models.TimeField(blank=True, null=True)),
                ('finish_time', models.TimeField(blank=True, null=True)),
                ('points', models.IntegerField(blank=True, null=True)),
                ('race_status', models.CharField(default='Finished', choices=[('DQ', 'DQ'), ('DNS', 'DNS'), ('DNF', 'DNF'), ('Finished', 'Finished')], max_length=40)),
                ('race', models.ForeignKey(to='main.Race')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='race',
            unique_together=set([('distance', 'title', 'date')]),
        ),
        migrations.AlterUniqueTogether(
            name='raceresult',
            unique_together=set([('athlete_name', 'race')]),
        ),
    ]
