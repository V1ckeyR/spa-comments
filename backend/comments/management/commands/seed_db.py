import random

from django.core.management.base import BaseCommand
from faker import Faker

from comments.models import User,Comment


class Command(BaseCommand):
    help = "Seed the database with test data"

    def handle(self, *args, **options):
        fake = Faker()

        self.stdout.write("1. Users...")
        users = []
        for _ in range(1000):
            users.append(User(
                username=fake.unique.user_name()[:30],
                email=fake.unique.email()
            ))

        created_users = list(User.objects.values_list('id', flat=True))
        self.stdout.write(f"Created {len(created_users)} users")

        self.stdout.write("2. Comments...")
        comments = []
        for _ in range(10000):
            comments.append(Comment(
                user_id=random.choice(created_users),
                content=fake.paragraph(nb_sentences=random.randint(1, 5)),
                created_at=fake.date_time_between(start_date='-1y', end_date='now'),
                updated_at=fake.date_time_between(start_date='-1y', end_date='now'),
            ))
        
        created_comments = Comment.objects.bulk_create(comments, ignore_conflicts=True, batch_size=500)
        self.stdout.write(f"Created {len(created_comments)} comments")

        self.stdout.write("3. Replies...")
        available_comments = list(Comment.objects.values_list('id', flat=True))
        TOTAL_REPLIES = 7000
        CHUNK_SIZE = 500
        
        for _ in range(0, TOTAL_REPLIES, CHUNK_SIZE):
            replies = []
            for _ in range(CHUNK_SIZE):
                is_reply = random.random() < 0.8
                parent_comment_id = random.choice(available_comments) if is_reply else None
                replies.append(Comment(
                    user_id=random.choice(created_users),
                    content=fake.paragraph(nb_sentences=random.randint(1, 5)),
                    reply_to_id=parent_comment_id,
                ))
            
            Comment.objects.bulk_create(replies, batch_size=CHUNK_SIZE)
            new_ids = list(Comment.objects.order_by('-id').values_list('id', flat=True)[:CHUNK_SIZE])
            available_comments.extend(new_ids)
            self.stdout.write(f"Created {len(new_ids)} replies")

        total_comments = Comment.objects.count()
        self.stdout.write(f"Total comments: {total_comments}")
