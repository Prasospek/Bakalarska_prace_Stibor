# Generated by Django 4.2.3 on 2023-07-11 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='suggestion',
            field=models.TextField(default='Your default suggestion', verbose_name='suggestion'),
        ),
    ]
