# Generated by Django 5.1.7 on 2025-03-19 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_expense_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
