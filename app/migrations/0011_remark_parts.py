# Generated by Django 4.1.1 on 2022-11-17 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_booking_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='remark',
            name='parts',
            field=models.CharField(default=1, max_length=255, verbose_name='検査部位'),
            preserve_default=False,
        ),
    ]