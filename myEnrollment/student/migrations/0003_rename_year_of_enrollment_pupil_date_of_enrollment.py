# Generated by Django 4.1.4 on 2023-05-24 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_alter_class_table'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pupil',
            old_name='year_of_enrollment',
            new_name='date_of_enrollment',
        ),
    ]
