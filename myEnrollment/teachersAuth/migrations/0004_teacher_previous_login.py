# Generated by Django 4.1.4 on 2023-01-02 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachersAuth', '0003_teacher_composite-pk-id-email'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='previous_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='previous login'),
        ),
    ]
