from django.core.management.base import BaseCommand
from puzzles.models import Puzzle
import datetime

class Command(BaseCommand):
    help = 'Deletes old puzzles from the database'

    def add_arguments(self, parser):
        parser.add_argument('--age', type=int, help='Delete puzzles older than this many days')
        parser.add_argument('--symbol', type=str, help='Delete puzzles for a specific symbol')
        parser.add_argument('--all', action='store_true', help='Delete all puzzles')
        parser.add_argument('--dry-run', action='store_true', help='Show which puzzles would be deleted without actually deleting them')

    def handle(self, *args, **options):
        age = options['age']
        symbol = options['symbol']
        delete_all = options['all']
        dry_run = options['dry_run']

        if not age and not symbol and not delete_all:
            self.stdout.write(self.style.ERROR('You must specify either --age, --symbol, or --all'))
            return

        queryset = Puzzle.objects.all()

        if age:
            cutoff_date = datetime.datetime.now() - datetime.timedelta(days=age)
            queryset = queryset.filter(created_at__lt=cutoff_date)

        if symbol:
            queryset = queryset.filter(symbol=symbol)

        if delete_all:
            queryset = Puzzle.objects.all()

        if dry_run:
            self.stdout.write(self.style.SUCCESS(f'Dry run: Found {queryset.count()} puzzles to delete.'))
            for puzzle in queryset:
                self.stdout.write(f'  - Would delete puzzle {puzzle.id} ({puzzle.symbol}, {puzzle.trend_type}, created at {puzzle.created_at})')
        else:
            count, _ = queryset.delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} puzzles.'))