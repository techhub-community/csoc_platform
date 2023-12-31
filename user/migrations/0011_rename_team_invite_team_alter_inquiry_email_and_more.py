# Generated by Django 4.2.2 on 2023-06-26 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0010_inquiry"),
    ]

    operations = [
        migrations.RenameField(
            model_name="invite",
            old_name="Team",
            new_name="team",
        ),
        migrations.AlterField(
            model_name="inquiry",
            name="email",
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name="inquiry",
            name="message",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="inquiry",
            name="name",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="inquiry",
            name="subject",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
