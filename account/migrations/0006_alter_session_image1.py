# Generated by Django 5.0 on 2024-04-20 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_membershipsession_total_sessions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='image1',
            field=models.FileField(default=1, upload_to='session/'),
            preserve_default=False,
        ),
    ]
