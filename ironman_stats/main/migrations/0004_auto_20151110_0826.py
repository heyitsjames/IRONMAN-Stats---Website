# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_race_race_id'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='raceresult',
            unique_together=set([]),
        ),
    ]
