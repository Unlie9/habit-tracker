# Generated by Django 5.0.7 on 2024-07-19 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habit_tracker', '0008_remove_userhabitdetail_completed_per_day_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='description',
            field=models.CharField(max_length=120),
        ),
        migrations.AlterField(
            model_name='habit',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
