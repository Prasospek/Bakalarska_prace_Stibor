# Generated by Django 4.2.3 on 2023-07-14 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxes', '0006_email_last_updated_email_message_email_sent_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='last_updated',
            field=models.DateTimeField(),
        ),
    ]
