# Generated by Django 5.1.7 on 2025-03-16 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicine', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicinepackage',
            name='conversion_factor',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
        ),
        migrations.AddField(
            model_name='medicinepackage',
            name='is_base_unit',
            field=models.BooleanField(default=False),
        ),
    ]
