from django.urls import path
from . import views

app_name = "puzzles"

urlpatterns = [
    path("",                          views.home,             name="home"),
    path("api/get_trend_puzzle/",     views.get_trend_puzzle, name="get_trend_puzzle"),
]
