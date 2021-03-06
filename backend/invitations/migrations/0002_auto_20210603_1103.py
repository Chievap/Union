# Generated by Django 3.1.7 on 2021-06-03 09:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('invitations', '0001_initial'),
        ('unions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='invite_acceptor',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='invite_acceptor',
                to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='invitation',
            name='invite_creator',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='invite_creator',
                to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='invitation',
            name='union',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to='unions.union'),
        ),
    ]
