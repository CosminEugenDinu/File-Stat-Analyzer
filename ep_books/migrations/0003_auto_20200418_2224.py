# Generated by Django 3.0.5 on 2020-04-18 22:24

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ep_analyze', '0004_auto_20200417_2155'),
        ('ep_books', '0002_auto_20200417_2155'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isbn', models.CharField(max_length=13)),
                ('google_isbn_info', django.contrib.postgres.fields.jsonb.JSONField()),
                ('files', models.ManyToManyField(to='ep_analyze.FileStat')),
            ],
        ),
        migrations.AddField(
            model_name='filecontentinfo',
            name='isbn',
            field=models.CharField(default='', max_length=13),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Documents',
        ),
    ]
