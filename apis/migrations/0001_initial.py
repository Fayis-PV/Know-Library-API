# Generated by Django 4.2.4 on 2023-08-17 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('url', models.URLField(max_length=500)),
                ('description', models.TextField()),
                ('image', models.URLField(blank=True, null=True)),
                ('banners', models.TextField(blank=True, null=True)),
                ('added_on', models.DateField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('category', models.ManyToManyField(to='apis.category')),
            ],
        ),
    ]