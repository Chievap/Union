# Generated by Django 3.2.3 on 2021-05-17 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unions', '0002_auto_20210421_1547'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='union',
            name='union_id',
        ),
        migrations.AlterField(
            model_name='union',
            name='name',
            field=models.TextField(primary_key=True, serialize=False),
        ),
    ]