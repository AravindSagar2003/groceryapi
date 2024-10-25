# Generated by Django 5.1.1 on 2024-10-21 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grocery', '0008_wishlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.CharField(max_length=50)),
                ('productname', models.CharField(max_length=50)),
                ('orderstatus', models.IntegerField(default=1)),
                ('price', models.CharField(max_length=50)),
                ('productid', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='images')),
            ],
        ),
    ]