# Generated by Django 4.1.1 on 2022-11-10 02:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_booking_category_booking_title_delete_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='category',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='remarks',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='title',
        ),
        migrations.CreateModel(
            name='Remark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_remarks', models.CharField(max_length=255, verbose_name='備考')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.category', verbose_name='カテゴリ')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='orders',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.remark', verbose_name='備考'),
            preserve_default=False,
        ),
    ]
