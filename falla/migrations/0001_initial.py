# Generated by Django 5.0.6 on 2024-11-18 06:37

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstacionSismografica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('ubicacion', models.CharField(max_length=255)),
                ('latitud', models.FloatField()),
                ('longitud', models.FloatField()),
                ('fecha_instalacion', models.DateField()),
                ('tipo', models.CharField(choices=[('Bajo costo', 'Bajo costo'), ('Estándar', 'Estándar')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, unique=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('telefono', models.CharField(blank=True, max_length=20, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='custom_user_set', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='custom_user_permissions_set', to='auth.permission', verbose_name='user permissions')),
                ('rol', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='falla.rol')),
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
            name='EventoSismico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('magnitud', models.FloatField()),
                ('profundidad', models.FloatField()),
                ('epicentro', models.CharField(max_length=255)),
                ('velocidad', models.FloatField()),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('estacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='falla.estacionsismografica')),
            ],
        ),
        migrations.CreateModel(
            name='Alerta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_alerta', models.DateTimeField(auto_now_add=True)),
                ('descripcion', models.TextField()),
                ('analista', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='falla.eventosismico')),
            ],
        ),
        migrations.CreateModel(
            name='Reporte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('descripcion', models.TextField()),
                ('analista', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('eventos_sismicos', models.ManyToManyField(to='falla.eventosismico')),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('Temperatura', 'Temperatura'), ('Movimiento', 'Movimiento')], max_length=50)),
                ('descripcion', models.TextField()),
                ('estacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sensores', to='falla.estacionsismografica')),
            ],
        ),
        migrations.CreateModel(
            name='UsuarioExtendido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='falla.rol')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
