# Generated by Django 5.0.3 on 2024-04-02 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0004_user_email_activation_user_is_admin_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="email_verification_code",
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]