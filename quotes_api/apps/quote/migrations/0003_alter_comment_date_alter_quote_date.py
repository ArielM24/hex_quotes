# Generated by Django 4.0.3 on 2022-03-19 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quote', '0002_alter_comment_comments_count_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='quote',
            name='date',
            field=models.DateTimeField(),
        ),
    ]