# Generated by Django 3.1.4 on 2021-02-26 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_theme'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Theme',
        ),
        migrations.AddField(
            model_name='customer',
            name='theme',
            field=models.CharField(choices=[('Light', 'Light'), ('Dark', 'Dark')], max_length=200, null=True),
        ),
    ]
