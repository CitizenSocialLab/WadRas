# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20181010_1524'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resident',
            name='updated_at',
        ),
    ]
