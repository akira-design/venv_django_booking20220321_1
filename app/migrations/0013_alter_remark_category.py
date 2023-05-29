# Generated by Django 4.1.1 on 2022-12-17 07:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_alter_remark_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remark',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='app.category', verbose_name='カテゴリ'),
        ),
    ]
