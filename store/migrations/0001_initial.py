# Generated by Django 4.1.5 on 2023-02-12 18:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import pyuploadcare.dj.models
import store.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('admins', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('thumbnail', models.FileField(blank=True, null=True, upload_to='')),
                ('order', models.IntegerField(default=0)),
                ('slug', models.SlugField(editable=False, max_length=225, verbose_name='Brand slug')),
                ('thumbnail_width', models.IntegerField(blank=True, null=True)),
                ('thumbnail_height', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='store.category')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_%(app_label)s.%(class)s_set+', to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name_plural': 'categories',
                'ordering': ('order', 'title'),
            },
        ),
        migrations.CreateModel(
            name='Consumer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=20)),
                ('mobile_number', models.IntegerField(blank=True, null=True)),
                ('address', models.CharField(max_length=200)),
                ('zip', models.IntegerField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(validators=[store.models.validate_description])),
                ('image', pyuploadcare.dj.models.ImageGroupField(blank=True)),
                ('available', models.IntegerField(blank=True, null=True)),
                ('price', models.FloatField(validators=[store.models.validate_price])),
                ('discount', models.FloatField(blank=True, null=True)),
                ('discount_duration', models.DateTimeField(blank=True, null=True)),
                ('Brand', models.CharField(blank=True, max_length=200, null=True)),
                ('attribute', models.ManyToManyField(blank=True, to='store.attribute')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.category')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admins.vendor')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_%(app_label)s.%(class)s_set+', to='contenttypes.contenttype')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='OrderedItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('processing', models.BooleanField(default=False)),
                ('consumer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.consumer')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordered_item', to='store.product')),
            ],
        ),
        migrations.AddField(
            model_name='consumer',
            name='wish_list',
            field=models.ManyToManyField(blank=True, to='store.product'),
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('transaction_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('completed', models.BooleanField(default=False)),
                ('date_ordered', models.DateTimeField(auto_now_add=True)),
                ('processing', models.BooleanField(default=False)),
                ('notes', models.TextField(blank=True)),
                ('consumer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.consumer')),
                ('items', models.ManyToManyField(blank=True, to='store.ordereditem')),
            ],
        ),
    ]
