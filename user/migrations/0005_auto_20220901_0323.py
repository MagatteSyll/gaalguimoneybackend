# Generated by Django 3.2.13 on 2022-08-31 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_user_is_staff_manager_personnel'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='lu',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='RetraitGaalguiShop',
        ),
    ]
