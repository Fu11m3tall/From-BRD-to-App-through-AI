# Generated by Django 5.2.1 on 2025-05-22 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brd', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brdvarity',
            options={'verbose_name': 'BRD Variety', 'verbose_name_plural': 'BRD Varieties'},
        ),
        migrations.AddField(
            model_name='brdvarity',
            name='description',
            field=models.TextField(default=''),
        ),
    ]
