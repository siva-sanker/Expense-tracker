# Generated by Django 5.1.7 on 2025-03-19 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_expense_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.FloatField()),
            ],
        ),
    ]
