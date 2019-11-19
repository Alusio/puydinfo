# Generated by Django 2.1.2 on 2019-08-20 12:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0036_calendar'),
    ]

    operations = [
        migrations.RenameField(
            model_name='calendar',
            old_name='name',
            new_name='rendering',
        ),
        migrations.RemoveField(
            model_name='calendar',
            name='json',
        ),
        migrations.AddField(
            model_name='calendar',
            name='allDay',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='calendar',
            name='color',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='blog.Color'),
        ),
        migrations.AddField(
            model_name='calendar',
            name='end',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='calendar',
            name='start',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='calendar',
            name='title',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
