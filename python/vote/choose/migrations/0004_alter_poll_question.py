# Generated by Django 4.2.16 on 2024-11-21 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('choose', '0003_remove_option_name_remove_option_total_votes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='question',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
