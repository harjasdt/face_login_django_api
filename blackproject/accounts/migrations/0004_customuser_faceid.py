# Generated by Django 4.2.4 on 2023-08-09 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_customuser_email_alter_customuser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='faceid',
            field=models.CharField(default=23, max_length=2000),
            preserve_default=False,
        ),
    ]
