# Generated by Django 5.1.1 on 2024-10-29 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grocery', '0012_alter_order_image_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='categoryimage',
            field=models.URLField(),
        ),
    ]
