# Generated by Django 4.1.1 on 2022-10-09 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_booking_modality'),
    ]

    operations = [
        migrations.AddField(
            model_name='modality',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images', verbose_name='イメージ画像'),
        ),
    ]
