# Generated by Django 5.1.1 on 2024-10-17 23:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grocery', '0002_registration_login_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registration',
            old_name='username',
            new_name='name',
        ),
    ]
