# Generated by Django 4.2.1 on 2023-06-01 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_information', '0007_remove_performance_tache_effectue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tache',
            name='deadline',
            field=models.DateTimeField(),
        ),
    ]
