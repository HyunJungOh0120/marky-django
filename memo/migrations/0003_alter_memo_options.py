# Generated by Django 3.2.6 on 2021-08-19 23:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('memo', '0002_alter_memo_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='memo',
            options={'ordering': ['-created_at']},
        ),
    ]