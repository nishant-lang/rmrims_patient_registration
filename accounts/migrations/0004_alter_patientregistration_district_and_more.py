# Generated by Django 5.1.2 on 2024-11-20 10:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_state_patientregistration_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientregistration',
            name='district',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.district'),
        ),
        migrations.AlterField(
            model_name='patientregistration',
            name='state',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.state'),
        ),
    ]