from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from .models import Puzzle
import random

@require_GET
def home(request):
    return render(request, "puzzles/index.html", {
        "puzzle": {
            "title": "Trend Trading Puzzle Simulator",
            "description": "Simulate trades on real uptrend/downtrend data from Binance."
        }
    })

@require_GET
def get_trend_puzzle(request):
    symbol = request.GET.get("symbol", "BTCUSDT")
    desired_trend = request.GET.get("trend", "uptrend")

    puzzles = Puzzle.objects.filter(symbol=symbol, trend_type=desired_trend)
    if not puzzles.exists():
        return JsonResponse({"error": "No puzzles found for this criteria."}, status=404)

    puzzle = random.choice(list(puzzles))

    return JsonResponse({
        "symbol": puzzle.symbol,
        "trend_type": puzzle.trend_type,
        "pre_trend": puzzle.pre_trend,
        "trend": puzzle.trend
    }, safe=False)
