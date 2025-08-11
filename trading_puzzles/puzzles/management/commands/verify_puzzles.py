from django.core.management.base import BaseCommand
from puzzles.models import Puzzle

class Command(BaseCommand):
    help = 'Verifies the puzzles in the database'

    def handle(self, *args, **options):
        puzzle_count = Puzzle.objects.count()
        self.stdout.write(self.style.SUCCESS(f'Found {puzzle_count} puzzles in the database.'))

        symbols = Puzzle.objects.values_list('symbol', flat=True).distinct()
        for symbol in symbols:
            count = Puzzle.objects.filter(symbol=symbol).count()
            self.stdout.write(f'  - {symbol}: {count} puzzles')