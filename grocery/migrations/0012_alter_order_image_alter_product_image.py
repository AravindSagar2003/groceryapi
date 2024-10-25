# Generated by Django 5.1.1 on 2024-10-24 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grocery', '0011_alter_order_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='image',
            field=models.ImageField(upload_to='images'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.URLField(),
        ),
    ]
