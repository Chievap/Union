# Generated by Django 3.1.7 on 2021-06-03 09:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('posts', '0001_initial'),
        ('unions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='union',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='unions.union'),
        ),
    ]
