# Generated by Django 5.1.7 on 2025-03-19 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_expense_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='price',
            field=models.DecimalField(decimal_places=10, max_digits=10),
        ),
    ]
