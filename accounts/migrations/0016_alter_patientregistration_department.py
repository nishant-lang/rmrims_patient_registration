# Generated by Django 5.1.2 on 2024-12-18 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_alter_patientregistration_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientregistration',
            name='department',
            field=models.CharField(choices=[('CLINICAL MEDICINE', 'Clinical Medicine'), ('PATHOLOGY', 'Pathology'), ('IMMUNOLOGY', 'Immunology'), ('MOLECULAR BIOLOGY', 'Molecular Biology'), ('BIOCHEMISTRY', 'Biochemistry')], default='CLINICAL MEDICINE', max_length=50),
        ),
    ]
