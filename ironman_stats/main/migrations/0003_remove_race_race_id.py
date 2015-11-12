# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_race_race_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='race',
            name='race_id',
        ),
    ]
