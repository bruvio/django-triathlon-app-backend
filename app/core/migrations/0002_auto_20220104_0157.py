# Generated by Django 3.2.10 on 2022-01-04 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='title',
            field=models.CharField(default='My Workout<function now at 0x7fb7c0923f70>', max_length=255),
        ),
        migrations.AlterField(
            model_name='activity',
            name='type',
            field=models.CharField(choices=[('workout', 'Workout'), ('race', 'Race'), ('wu', 'Warm Up'), ('cd', 'Cool Down')], default='workout', max_length=255),
        ),
    ]