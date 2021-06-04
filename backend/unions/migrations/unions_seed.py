# Generated by Django 3.1.7 on 2021-06-04 16:30
import logging
from random import random, choice

from django.db import migrations
from django.utils.timezone import now

from unions.models import Union, UnionUsersManager, UnionUsers
from unions.serializer import UnionSerializer
from users.models import User


def create_unions(a, b):
    """Create unions"""
    logging.info("Creating unions")
    # sha256 hash of 'testpass'
    titles = ["Bound Mist",
              "The Magnificent Servant",
              "Thorns of Waves",
              "The Emerald's End",
              "The Hunter of the Sword",
              "Slaves in the Sparks",
              "An Introduction to Crypto",
              "Sleeping Slaves",
              "The Touch of the Voyagers",
              "Light in the Soul"
              ]

    for i in range(len(titles)):
        random_user = choice(list(User.objects.all()))
        union = {
            "name": titles[i],
            "description": 'Donec sollicitudin molestie malesuada. Curabitur arcu erat, accumsan id imperdiet et, porttitor at sem. Vivamus magna justo, lacinia eget consectetur sed, convallis at tellus. Vivamus suscipit tortor eget felis porttitor volutpat. Vivamus suscipit tortor eget felis porttitor volutpat. Vivamus magna justo, lacinia eget consectetur sed, convallis at tellus.',
            "members_can_invite": True if random() > 0.5 else False,
            "icon": "https://banner2.cleanpng.com/20180123/gjq/kisspng-bitcoin-cash-cryptocurrency-icon-5a68081d193577.7421991315167672611033.jpg",
            "banner": "https://i1.wp.com/www.snowdropsolution.com/wp-content/uploads/2020/09/4-Simple-Use-Of-Natural-Language-Processing-In-Businesses.jpg?resize=640%2C360&ssl=1",
            "creator_id": random_user.user_id,
            "created_at": now()
        }

        ser = UnionSerializer(data=union)
        ser.is_valid(raise_exception=True)
        ser.save()
        logging.info(f"{union} union created.")

        # Connecting some users to other the unions
        user_count = User.objects.all().count()
        for i in range(int(user_count / 2)):
            random_union = choice(list(Union.objects.all()))
            random_user = choice(list(User.objects.all()))
            UnionUsers.objects.create(union=random_union, user=random_user)

    return True


class Migration(migrations.Migration):
    dependencies = [
        ('unions', '0002_auto_20210603_1103'),
        ('users', 'users_seed'),
    ]

    operations = [
        migrations.RunPython(create_unions),
    ]
