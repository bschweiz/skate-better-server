# Generated by Django 3.1.7 on 2021-03-23 16:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('skatebetterapi', '0002_auto_20210318_2000'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='won',
        ),
        migrations.AlterField(
            model_name='game',
            name='skater',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='skatebetterapi.skater'),
        ),
    ]
