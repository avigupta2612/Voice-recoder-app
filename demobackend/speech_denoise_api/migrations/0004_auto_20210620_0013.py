# Generated by Django 3.2.4 on 2021-06-19 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('speech_denoise_api', '0003_speech2text'),
    ]

    operations = [
        migrations.RenameField(
            model_name='audiofile',
            old_name='input_audio',
            new_name='input_audio_wav',
        ),
        migrations.AddField(
            model_name='audiofile',
            name='input_audio_other',
            field=models.FileField(blank=True, null=True, upload_to='input-audio'),
        ),
    ]