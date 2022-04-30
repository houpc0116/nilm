# Generated by Django 3.2.10 on 2022-03-24 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Redd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('pw', models.FloatField()),
                ('device', models.CharField(max_length=100)),
                ('house', models.IntegerField()),
            ],
            options={
                'db_table': 'redd',
                'managed': False,
            },
        ),
    ]
