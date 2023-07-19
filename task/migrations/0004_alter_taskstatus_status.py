# Generated by Django 4.2.2 on 2023-07-19 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_task_task_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskstatus',
            name='status',
            field=models.CharField(choices=[('PEN', 'PENDING'), ('SUB', 'SUBMITTED'), ('VER', 'VERIFIED')], default='PEN', max_length=3),
        ),
    ]