# Generated by Django 4.1.2 on 2023-04-09 01:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_student_addfield'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='addField',
        ),
    ]
