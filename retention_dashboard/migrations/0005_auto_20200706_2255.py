# Generated by Django 2.2.12 on 2020-07-06 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retention_dashboard', '0004_auto_20200521_0108'),
    ]

    operations = [
        migrations.AddField(
            model_name='datapoint',
            name='has_a_term',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='datapoint',
            name='has_b_term',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='datapoint',
            name='has_full_term',
            field=models.BooleanField(default=False),
        ),
    ]
