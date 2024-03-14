# Generated by Django 3.2.6 on 2024-03-14 21:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import reserve.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('name', models.CharField(max_length=250)),
                ('username', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('name_complete', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('web', models.URLField()),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=250)),
                ('services', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Campus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campus_name', models.CharField(max_length=250, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Space',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('capacity', models.IntegerField()),
                ('general_info', models.TextField()),
                ('schedule', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reserve.building')),
                ('features', models.ManyToManyField(blank=True, to='reserve.Equipment')),
            ],
        ),
        migrations.CreateModel(
            name='Space_item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('image', models.ImageField(blank=True, null=True, upload_to=reserve.models.user_directory_path)),
                ('seat_status', models.IntegerField(choices=[(0, 'FREE'), (1, 'RESERVED'), (2, 'EXPIRED'), (3, 'DISABLED')], default=0)),
                ('space_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reserve.space')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('space_item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reserve.space_item')),
                ('capacity', models.IntegerField()),
            ],
            bases=('reserve.space_item',),
        ),
        migrations.AddField(
            model_name='building',
            name='campus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reserve.campus'),
        ),
        migrations.CreateModel(
            name='Desk',
            fields=[
                ('space_item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reserve.space_item')),
                ('nearby_pl', models.ManyToManyField(blank=True, related_name='_reserve_desk_nearby_pl_+', to='reserve.Desk')),
            ],
            bases=('reserve.space_item',),
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_time', models.DateTimeField()),
                ('duration', models.DurationField()),
                ('end_time', models.DateTimeField()),
                ('building', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='reserve.building')),
                ('campus', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='reserve.campus')),
                ('space', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='reserve.space')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('desk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reserve.desk')),
            ],
        ),
    ]
