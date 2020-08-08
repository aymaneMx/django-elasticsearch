import random

from dateutil.tz import tz
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand
from faker import Faker

from posts.models import Post, Reply

# config
User = get_user_model()


class Command(BaseCommand):
    help = 'Create random posts'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Indicates the number of posts to be created')
        parser.add_argument('-r', '--replies', action='store_true', help='Creates replies')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        replies = kwargs['replies']
        faker = Faker()

        # create a super user + other simple users
        User.objects.create_superuser("admin", "admin@admin.com", "admin")
        [create_profile(faker) for _ in range(4)]

        users_ids = User.objects.values_list('id', flat=True)

        # create posts
        for _ in range(count):
            create_post(faker, users_ids, replies)

        call_command('search_index', '--rebuild', '-f')
        self.stdout.write(self.style.SUCCESS('Successfully ended commands'))


def create_profile(faker, retries=0):
    username = faker.user_name()

    if not User.objects.filter(username=username).exists():
        user = User(username=username, email=faker.email())
        user.set_password(faker.password())
        user.save()
        return user

    elif retries < 3:
        # try again with different random username
        return create_profile(faker, retries + 1)


def create_post(faker, users_ids, replies):
    post = Post(
        title=faker.text(60),
        user_id=random.choice(users_ids),
        content=faker.text(random.randint(100, 1000)),
        created_at=faker.date_time_between(start_date="-10d", end_date="now", tzinfo=tz.gettz('UTC')),
        draft=False,
    )
    post.save()

    if replies:
        add_random_replies(faker, post.id, users_ids)


def add_random_replies(faker, post_id, users_ids):
    for _ in range(random.randrange(5)):
        reply = Reply(
            content=faker.text(random.randint(10, 500)),
            user_id=random.choice(users_ids),
            post_id=post_id
        )
        reply.save()
