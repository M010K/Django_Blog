# Generated by Django 2.2.3 on 2021-06-27 13:15

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
