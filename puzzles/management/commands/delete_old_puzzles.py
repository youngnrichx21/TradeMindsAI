import time
from django.core.management.base import BaseCommand
from puzzles.models import Puzzle
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Deletes old puzzles from the database.'

    def add_arguments(self, parser):
        parser.add_argument('--days', type=int, default=30, help='The number of days to keep puzzles.')
        parser.add_argument('--dry-run', action='store_true', help='If set, the command will only list the puzzles to be deleted.')

    def handle(self, *args, **options):
        days_to_keep = options['days']
        dry_run = options['dry_run']

        cutoff_date = datetime.now() - timedelta(days=days_to_keep)

        self.stdout.write(f'Looking for puzzles older than {cutoff_date}...')

        puzzles_to_delete = Puzzle.objects.filter(created_at__lt=cutoff_date)

        if dry_run:
            self.stdout.write(f'Found {puzzles_to_delete.count()} puzzles to delete:')
            for puzzle in puzzles_to_delete:
                self.stdout.write(f'  - Puzzle {puzzle.id} ({puzzle.symbol}) created at {puzzle.created_at}')
        else:
            count = puzzles_to_delete.count()
            puzzles_to_delete.delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} puzzles.'))