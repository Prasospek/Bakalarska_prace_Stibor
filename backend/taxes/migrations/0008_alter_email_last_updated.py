# Generated by Django 4.2.3 on 2023-07-14 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxes', '0007_alter_email_last_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
