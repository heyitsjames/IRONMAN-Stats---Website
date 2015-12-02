# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20151110_0826'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComputedRaceData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('age_group', models.CharField(max_length=255, choices=[('Pro', 'Pro'), ('18-24', '18-24'), ('25-29', '25-29'), ('30-34', '30-34'), ('35-39', '35-39'), ('40-44', '40-44'), ('45-49', '45-49'), ('50-54', '50-54'), ('55-59', '55-59'), ('60-64', '60-64'), ('65-69', '65-69'), ('70-74', '70-74'), ('75-79', '75-79'), ('80-999', '80-999')])),
                ('sex', models.CharField(max_length=1, choices=[('M', 'M'), ('F', 'F')])),
                ('average_swim_time', models.TimeField(null=True, blank=True)),
                ('average_bike_time', models.TimeField(null=True, blank=True)),
                ('average_run_time', models.TimeField(null=True, blank=True)),
                ('average_finish_time', models.TimeField(null=True, blank=True)),
                ('race', models.ForeignKey(to='main.Race')),
            ],
        ),
    ]
