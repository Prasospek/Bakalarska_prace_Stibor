# Generated by Django 4.2.3 on 2023-10-01 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxes', '0009_remove_email_last_updated'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('Dividend', 'Dividend'), ('MarketSell', 'Market Sell'), ('InterestOnCash', 'Interest on Cash'), ('Withdrawal', 'Withdrawal')], max_length=20)),
                ('date', models.DateTimeField()),
                ('isin', models.CharField(max_length=20)),
                ('ticker', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=255)),
                ('shares', models.DecimalField(decimal_places=4, max_digits=10)),
                ('price_per_share', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(max_length=10)),
                ('exchange_rate', models.DecimalField(decimal_places=4, max_digits=10, null=True)),
                ('result', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('withholding_tax', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('charge_amount', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
