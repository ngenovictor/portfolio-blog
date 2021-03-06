# Generated by Django 3.0.3 on 2020-02-07 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('title', models.TextField()),
                ('image', models.TextField()),
                ('summary', models.TextField()),
                ('content', models.TextField()),
                ('date_created', models.TimeField(auto_now_add=True)),
                ('date_updated', models.TimeField(auto_now=True)),
            ],
        ),
    ]
