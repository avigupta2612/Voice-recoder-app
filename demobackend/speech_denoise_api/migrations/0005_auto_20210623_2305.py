# Generated by Django 3.2.4 on 2021-06-23 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('speech_denoise_api', '0004_auto_20210620_0013'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Speech2Text',
        ),
        migrations.AlterField(
            model_name='audiofile',
            name='userId',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]