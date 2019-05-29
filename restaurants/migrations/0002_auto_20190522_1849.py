# Generated by Django 2.1.7 on 2019-05-22 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='notes',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='dish',
            name='rating',
            field=models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)], default=0),
        ),
    ]
