# Generated by Django 4.1.4 on 2023-01-09 14:59

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields
import teachersAuth.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Canton',
            fields=[
                ('_canton_code', models.CharField(default='ZDK', max_length=3, primary_key=True, serialize=False)),
                ('canton_name', models.CharField(default='Zenicko-dobojski', max_length=50)),
                ('country', django_countries.fields.CountryField(default='BA', max_length=2)),
            ],
            options={
                'db_table': 'cantons',
            },
        ),
        migrations.CreateModel(
            name='SecondarySchool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_name', models.CharField(default='Tehnicka skola Zenica', max_length=100, unique=True)),
                ('school_address', models.CharField(default='Bilimisce 28, Zenica', max_length=100)),
                ('school_canton_code', models.ForeignKey(default='ZDK', on_delete=django.db.models.deletion.CASCADE, related_name='school_canton', to='teachersAuth.canton')),
            ],
            options={
                'db_table': 'secondarySchools',
            },
        ),
        migrations.CreateModel(
            name='CoursesSecondarySchool',
            fields=[
                ('_course_code', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('course_name', models.CharField(max_length=100)),
                ('course_duration', models.CharField(choices=[('III', 'Trogodisnje'), ('IV', 'Cetverogodisnje')], default='IV', max_length=10)),
                ('school_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses_secondary', to='teachersAuth.secondaryschool')),
            ],
            options={
                'db_table': 'courses_secondary',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('previous_login', models.DateTimeField(blank=True, null=True, verbose_name='previous login')),
                ('course_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_code', to='teachersAuth.coursessecondaryschool')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('school_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='school_id', to='teachersAuth.secondaryschool')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Nastavnik',
                'verbose_name_plural': 'Nastavnici',
                'db_table': 'teachers',
                'ordering': ['email'],
            },
            managers=[
                ('objects', teachersAuth.models.CustomUserManager()),
            ],
        ),
        migrations.AddConstraint(
            model_name='coursessecondaryschool',
            constraint=models.UniqueConstraint(fields=('school_id', '_course_code'), name='composite-pk-school_id-course_code'),
        ),
        migrations.AddConstraint(
            model_name='teacher',
            constraint=models.UniqueConstraint(fields=('id', 'email', 'course_code'), name='composite-pk-id-email-course'),
        ),
    ]
