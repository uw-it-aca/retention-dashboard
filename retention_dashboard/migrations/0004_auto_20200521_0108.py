# Generated by Django 2.2.12 on 2020-05-21 01:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('retention_dashboard', '0003_auto_20200520_0016'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='advisor',
            unique_together={('advisor_netid', 'advisor_type')},
        ),
    ]
