# Generated by Django 4.2.16 on 2024-11-21 00:40

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wishlist', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wishlist',
            old_name='product_code',
            new_name='fin_prdt_cd',
        ),
        migrations.RenameField(
            model_name='wishlist',
            old_name='product_name',
            new_name='fin_prdt_nm',
        ),
        migrations.RenameField(
            model_name='wishlist',
            old_name='bank_name',
            new_name='kor_co_nm',
        ),
        migrations.RenameField(
            model_name='wishlist',
            old_name='maturity_term',
            new_name='mtrt_int',
        ),
        migrations.AlterUniqueTogether(
            name='wishlist',
            unique_together={('user', 'fin_prdt_cd')},
        ),
    ]
