# Generated by Django 2.2.10 on 2020-11-01 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0004_metroarea_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='price',
            field=models.IntegerField(choices=[(1, '$'), (2, '$$'), (3, '$$$'), (4, '$$$$'), (5, '$$$$$')], default=1, help_text='$ = <10, $$ = 11-25, $$$ = 26-50, $$$$ = 51-100, $$$$$ = >100'),
        ),
    ]
