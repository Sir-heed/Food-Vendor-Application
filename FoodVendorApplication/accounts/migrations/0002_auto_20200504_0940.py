# Generated by Django 3.0.5 on 2020-05-04 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auth',
            old_name='is_Active',
            new_name='isActive',
        ),
    ]
