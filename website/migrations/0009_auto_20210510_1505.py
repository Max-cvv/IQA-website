# Generated by Django 2.0 on 2021-05-10 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_tiaomu'),
    ]

    operations = [
        migrations.AddField(
            model_name='records',
            name='co1',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='records',
            name='co2',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='records',
            name='device1',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='records',
            name='device2',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
