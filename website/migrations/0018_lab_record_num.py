# Generated by Django 2.0 on 2021-06-18 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0017_lab_user_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='lab',
            name='record_num',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
