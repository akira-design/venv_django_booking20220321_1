# Generated by Django 4.1.1 on 2022-12-22 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_alter_booking_orders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remark',
            name='order_remarks',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='備考'),
        ),
    ]