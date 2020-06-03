# Generated by Django 3.0.5 on 2020-04-17 21:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ep_analyze', '0003_auto_20200406_1446'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilesRelatives',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('by_size', models.IntegerField()),
                ('by_name', models.IntegerField()),
                ('close_match_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='close_math_id', to='ep_analyze.FileStat')),
                ('file_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file_id', to='ep_analyze.FileStat')),
            ],
            options={
                'unique_together': {('file_id', 'close_match_id')},
            },
        ),
        migrations.DeleteModel(
            name='FileStatTest',
        ),
    ]
