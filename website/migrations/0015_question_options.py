# Generated by Django 2.0 on 2021-05-26 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_lab'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='options',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]