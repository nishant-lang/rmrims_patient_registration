# Generated by Django 5.1.2 on 2024-12-18 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_alter_patientregistration_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientregistration',
            name='department',
            field=models.CharField(choices=[('CLINICAL MEDICINE', 'Clinical Medicine'), ('PATHOLOGY', 'Pathology'), ('IMMUNOLOGY', 'Immunology'), ('MOLECULAR BIOLOGY', 'Molecular Biology'), ('BIOCHEMISTRY', 'Biochemistry')], default='CLINICAL_MEDICINE', max_length=50),
        ),
    ]