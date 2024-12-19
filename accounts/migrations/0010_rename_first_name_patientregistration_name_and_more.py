# Generated by Django 5.1.2 on 2024-11-25 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_patientregistration_middle_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patientregistration',
            old_name='first_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='patientregistration',
            name='date_of_birth',
        ),
        migrations.RemoveField(
            model_name='patientregistration',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='patientregistration',
            name='middle_name',
        ),
        migrations.AddField(
            model_name='patientregistration',
            name='age',
            field=models.CharField(default=0, max_length=100),
        ),
        migrations.AlterField(
            model_name='patientregistration',
            name='department',
            field=models.CharField(choices=[('CLINICAL_MEDICINE', 'Clinical Medicine'), ('PATHOLOGY', 'Pathology'), ('IMMUNOLOGY', 'Immunology'), ('MOLECULAR_BIOLOGY', 'Molecular Biology'), ('BIOCHEMISTRY', 'Biochemistry')], default='CLINICAL_MEDICINE', max_length=50),
        ),
    ]
