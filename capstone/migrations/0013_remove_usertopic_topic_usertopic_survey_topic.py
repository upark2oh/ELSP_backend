# Generated by Django 4.2.7 on 2023-11-23 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('capstone', '0012_alter_surveyquiz_topic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usertopic',
            name='topic',
        ),
        migrations.AddField(
            model_name='usertopic',
            name='survey_topic',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='capstone.surveyquiz'),
            preserve_default=False,
        ),
    ]