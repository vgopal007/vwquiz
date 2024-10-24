from django.core.management.base import BaseCommand
from quizapp.models import QuizSession
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Remove QuizSession entries with invalid user references'

    def handle(self, *args, **kwargs):
        # Get all QuizSession instances with invalid user references
        invalid_sessions = QuizSession.objects.filter(user_id__isnull=False).exclude(user_id__in=User.objects.values_list('id', flat=True))

        # Count the number of invalid sessions to be deleted
        count_invalid = invalid_sessions.count()

        # Delete the invalid QuizSession instances
        if count_invalid > 0:
            invalid_sessions.delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count_invalid} invalid quiz sessions.'))
        else:
            self.stdout.write(self.style.WARNING('No invalid quiz sessions found.'))
