# Generated by Django 2.0 on 2021-04-24 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_records_submit_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField()),
                ('isGlasses', models.IntegerField()),
                ('gender', models.IntegerField()),
                ('edu', models.IntegerField()),
                ('pho', models.IntegerField()),
                ('screen', models.CharField(blank=True, max_length=60, null=True)),
            ],
        ),
    ]
