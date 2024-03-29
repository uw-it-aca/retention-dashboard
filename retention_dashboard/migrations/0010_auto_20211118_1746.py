# Generated by Django 2.2.19 on 2021-11-18 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retention_dashboard', '0009_auto_20210624_1610'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sport_code', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='datapoint',
            name='sports',
            field=models.ManyToManyField(null=True, to='retention_dashboard.Sport'),
        ),
    ]
