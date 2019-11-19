# Generated by Django 2.1.2 on 2019-07-12 11:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Fact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Familly',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                (
                'user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('slug', models.CharField(blank=True, max_length=30)),
                ('content', models.TextField(blank=True)),
                ('photo_banner', models.ImageField(blank=True, null=True, upload_to='banner')),
                ('photo_home', models.ImageField(blank=True, null=True, upload_to='show_hom')),
                ('category', models.ManyToManyField(to='blog.Category')),
                ('color_title', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING,
                                                  to='blog.Color')),
            ],
        ),
        migrations.CreateModel(
            name='Image_Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='show')),
                ('author', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Image_Show',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='show')),
                ('author', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='New',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30)),
                ('content', models.TextField(blank=True)),
                ('url', models.CharField(blank=True, max_length=30)),
                ('maj', models.CharField(blank=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Price_exact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minimum', models.IntegerField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Programme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resultat', models.TextField(blank=True)),
                ('resultat_im', models.TextField(blank=True)),
                ('hor_finder', models.TextField(blank=True)),
                ('freq_temps', models.TextField(blank=True)),
                ('temps', models.TextField(blank=True)),
                ('size', models.TextField(blank=True)),
                ('restaurant_rapide', models.TextField(blank=True)),
                ('coef_unmissable', models.TextField(blank=True)),
                ('date', models.DateField(auto_now=True)),
                (
                'user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30)),
                ('content', models.TextField(blank=True)),
                ('author', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('slug', models.CharField(blank=True, max_length=30)),
                ('content', models.TextField(blank=True)),
                ('photo_banner', models.ImageField(blank=True, null=True, upload_to='banner')),
                ('photo_home', models.ImageField(blank=True, null=True, upload_to='show_hom')),
                ('num_plan', models.CharField(blank=True, max_length=1)),
                ('category', models.ManyToManyField(to='blog.Category')),
                ('color_title', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING,
                                                  to='blog.Color')),
                ('price', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING,
                                            to='blog.Price')),
            ],
        ),
        migrations.CreateModel(
            name='Sejour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Spectacle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('slug', models.CharField(blank=True, max_length=30)),
                ('content', models.TextField(blank=True)),
                ('duration', models.IntegerField(blank=True, null=True)),
                ('capacity', models.IntegerField(blank=True, null=True)),
                ('photo_banner', models.ImageField(blank=True, null=True, upload_to='banner')),
                ('photo_home', models.ImageField(blank=True, null=True, upload_to='show_hom')),
                ('category', models.ManyToManyField(to='blog.Category')),
                ('color_title', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING,
                                                  to='blog.Color')),
            ],
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='spectacle',
            name='theme',
            field=models.ManyToManyField(to='blog.Theme'),
        ),
        migrations.AddField(
            model_name='spectacle',
            name='type',
            field=models.ManyToManyField(to='blog.Type'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='theme',
            field=models.ManyToManyField(to='blog.Theme'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='type',
            field=models.ManyToManyField(to='blog.Type'),
        ),
        migrations.AddField(
            model_name='quote',
            name='show_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING,
                                    to='blog.Spectacle'),
        ),
        migrations.AddField(
            model_name='profile',
            name='show_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING,
                                    to='blog.Spectacle'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='image_show',
            name='show_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING,
                                    to='blog.Spectacle'),
        ),
        migrations.AddField(
            model_name='image_restaurant',
            name='restaurant_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING,
                                    to='blog.Restaurant'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='price',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING,
                                    to='blog.Price'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='theme',
            field=models.ManyToManyField(to='blog.Theme'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='type',
            field=models.ManyToManyField(to='blog.Type'),
        ),
        migrations.AddField(
            model_name='fact',
            name='show_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING,
                                       to='blog.Spectacle'),
        ),
    ]
