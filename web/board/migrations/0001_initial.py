# Generated by Django 4.2.2 on 2023-07-06 07:34

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('position', models.CharField(choices=[('관리자', '관리자'), ('감독', '감독'), ('반장', '반장')], max_length=30, null=True)),
                ('address', models.CharField(max_length=200)),
                ('call', models.CharField(max_length=20)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Accident',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ac_area', models.CharField(max_length=50)),
                ('ac_status', models.CharField(choices=[('사고발생', '사고발생'), ('조치 중', '조치 중'), ('조치완료', '조치완료')], max_length=30, null=True)),
                ('img', models.ImageField(upload_to='')),
                ('ac_cont', models.TextField(null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cmp', models.CharField(max_length=40)),
                ('emp_name', models.CharField(max_length=20)),
                ('position', models.CharField(max_length=20)),
                ('work', models.CharField(max_length=20)),
                ('emp_call', models.CharField(max_length=20)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('address', models.CharField(max_length=200)),
                ('img', models.ImageField(upload_to='')),
                ('work_area', models.CharField(max_length=100)),
                ('start_time', models.DateField(blank=True, null=True)),
                ('end_time', models.DateField(blank=True, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('serial_num', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Fieldlog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fl_area', models.CharField(max_length=100)),
                ('fl_status', models.CharField(max_length=100)),
                ('img', models.ImageField(upload_to='')),
                ('fl_cont', models.TextField(null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Wearable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hook', models.IntegerField(choices=[(1, '미체결'), (2, '불량체결'), (0, '체결')], null=True)),
                ('altitude', models.FloatField()),
                ('battery', models.IntegerField(null=True)),
                ('degree_safety', models.IntegerField(choices=[(3, '경계'), (4, '심각'), (1, '관심'), (0, '양호'), (2, '주의')], null=True)),
                ('event', models.IntegerField(null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Safety',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scl_area', models.CharField(max_length=50)),
                ('scl_status', models.CharField(choices=[('심각', '심각'), ('양호', '양호'), ('주의', '주의')], max_length=30, null=True)),
                ('img', models.ImageField(upload_to='')),
                ('scl_cont', models.TextField(null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Replay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contents', models.TextField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('fieldlog', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='board.fieldlog')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='board.accident')),
                ('safety', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='board.safety')),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LogRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('action', models.CharField(max_length=50)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pair', models.IntegerField(null=True)),
                ('employee1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_employee1', to='board.employee')),
                ('employee2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_employee2', to='board.employee')),
            ],
        ),
    ]
