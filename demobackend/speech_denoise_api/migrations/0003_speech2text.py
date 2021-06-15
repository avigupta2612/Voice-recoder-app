# Generated by Django 3.2.4 on 2021-06-15 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('speech_denoise_api', '0002_alter_audiofile_userid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Speech2Text',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_audio', models.FileField(upload_to='s2t_audio')),
            ],
        ),
    ]
