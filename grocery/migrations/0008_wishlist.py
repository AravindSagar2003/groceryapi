# Generated by Django 5.1.1 on 2024-10-20 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grocery', '0007_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.CharField(max_length=50)),
                ('productname', models.CharField(max_length=50)),
                ('Wishliststatus', models.CharField(default=1, max_length=50)),
                ('price', models.CharField(max_length=50)),
                ('productid', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='images')),
            ],
        ),
    ]