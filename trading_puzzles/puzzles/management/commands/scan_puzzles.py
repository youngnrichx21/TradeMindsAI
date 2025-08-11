import requests, datetime
from django.core.management.base import BaseCommand
from puzzles.models import Puzzle

class Command(BaseCommand):
    help = 'Scans for new trend puzzles and saves them to the database'

    def handle(self, *args, **options):
        symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
        for symbol in symbols:
            self.stdout.write(f'Scanning {symbol}...')
            self.scan_symbol(symbol)

    def scan_symbol(self, symbol):
        # This is a simplified scanner. A production system would be more robust.
        # It would handle pagination, rate limits, and errors more gracefully.
        end_ms = int(datetime.datetime.utcnow().timestamp() * 1000)
        for _ in range(5): # Scan last 5000 minutes
            start_ms = end_ms - (1000 * 60 * 1000)
            try:
                resp = requests.get(
                    "https://api.binance.com/api/v3/klines",
                    params={
                        "symbol": symbol,
                        "interval": "1m",
                        "startTime": start_ms,
                        "endTime": end_ms,
                        "limit": 1000
                    }
                )
                resp.raise_for_status()
                raw_candles = resp.json()
                candles = [{
                    "time": k[0]//1000,
                    "open": float(k[1]),
                    "high": float(k[2]),
                    "low": float(k[3]),
                    "close": float(k[4])
                } for k in raw_candles]

                self.find_and_save_puzzles(symbol, candles)

            except requests.exceptions.RequestException as e:
                self.stderr.write(self.style.ERROR(f'Error fetching data for {symbol}: {e}'))
                break
            
            end_ms = start_ms

    def find_and_save_puzzles(self, symbol, candles):
        self.stdout.write(f'  - Analyzing {len(candles)} candles for {symbol}')
        window = 30
        puzzles_found = 0
        for i in range(len(candles) - window + 1):
            seg = candles[i:i+window]
            if self.is_up(seg):
                self.save_puzzle(symbol, 'uptrend', candles[:i], seg)
                puzzles_found += 1
            elif self.is_down(seg):
                self.save_puzzle(symbol, 'downtrend', candles[:i], seg)
                puzzles_found += 1
        if puzzles_found == 0:
            self.stdout.write(self.style.WARNING(f'  - No puzzles found in this batch for {symbol}'))

    def save_puzzle(self, symbol, trend_type, pre_trend, trend):
        Puzzle.objects.create(
            symbol=symbol,
            trend_type=trend_type,
            pre_trend=pre_trend,
            trend=trend
        )
        self.stdout.write(self.style.SUCCESS(f'Saved {trend_type} puzzle for {symbol}'))

    def is_up(self, seg):
        # A less stringent check for an uptrend.
        # The high of the last candle must be the highest in the segment,
        # and the low of the first candle must be the lowest.
        # This allows for some noise/consolidation within the trend.
        if not seg:
            return False
        return seg[-1]["high"] == max(c["high"] for c in seg) and seg[0]["low"] == min(c["low"] for c in seg)

    def is_down(self, seg):
        # A less stringent check for a downtrend.
        # The low of the last candle must be the lowest in the segment,
        # and the high of the first candle must be the highest.
        if not seg:
            return False
        return seg[-1]["low"] == min(c["low"] for c in seg) and seg[0]["high"] == max(c["high"] for c in seg)