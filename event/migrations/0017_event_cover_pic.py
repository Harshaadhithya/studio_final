# Generated by Django 4.0.4 on 2022-06-22 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0016_eventphotos'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='cover_pic',
            field=models.ImageField(blank=True, null=True, upload_to='event_images/'),
        ),
    ]
