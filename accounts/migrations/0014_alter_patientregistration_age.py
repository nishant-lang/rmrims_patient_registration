# Generated by Django 5.1.2 on 2024-12-12 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_alter_patientregistration_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientregistration',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]