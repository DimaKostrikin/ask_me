# Generated by Django 3.1.3 on 2020-11-17 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default=2, upload_to='200.jpg', verbose_name='Аватарка'),
            preserve_default=False,
        ),
    ]
