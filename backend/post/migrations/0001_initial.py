# Generated by Django 3.1.7 on 2021-03-17 09:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('union', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('post_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.TextField()),
                ('message', models.TextField()),
                ('upvotes', models.IntegerField()),
                ('downvotes', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('union_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='union.union')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
