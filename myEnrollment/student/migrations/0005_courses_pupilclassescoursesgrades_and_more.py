# Generated by Django 4.1.4 on 2023-05-24 15:01

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_pupil_composite-pk-name-last_name-address_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('course_code', models.CharField(max_length=5, primary_key=True, serialize=False, unique=True)),
                ('course_name', models.CharField(blank=True, max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PupilClassesCoursesGrades',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(5)])),
                ('pupil_behavior', models.CharField(choices=[('5', 'odlican'), ('4', 'vrlo dobar'), ('3', 'dobar'), ('2', 'zadovoljava')], max_length=10)),
                ('class_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pupil_class_id', to='student.class')),
                ('course_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pupil_courses_code', to='student.courses')),
                ('pupil_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pupil_id', to='student.pupil')),
            ],
            options={
                'db_table': 'PupilClassesCoursesGrades',
            },
        ),
        migrations.DeleteModel(
            name='PupilClassesGrades',
        ),
        migrations.AddConstraint(
            model_name='pupilclassescoursesgrades',
            constraint=models.UniqueConstraint(fields=('pupil_id', 'class_id', 'course_code'), name='composite-pk-pupil_id-class_id-course_code'),
        ),
    ]
