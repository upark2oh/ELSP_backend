# Generated by Django 4.2.7 on 2023-11-23 19:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('capstone', '0015_alter_usertopic_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='usertopic',
            unique_together=set(),
        ),
    ]