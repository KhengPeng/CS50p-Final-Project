import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
from nba_api.stats.static import players
from nba_api.stats.endpoints import playerprofilev2
import pytest
from nba_api_project import Player, number_of_players, statistics_per_game_basis, statistics_to_analyse_for_x_axis


def test_init_():
    test_player = Player()
    assert test_player.name == "Kobe Bryant"
    assert test_player.age == 35
    assert test_player.season == "regular season"

    test_player = Player("Lebron James", 36, "playoffs")
    assert test_player.name == "Lebron James"
    assert test_player.age == 36
    assert test_player.season == "playoffs"


def test_number_of_players(monkeypatch):
    with pytest.raises(TypeError):
        number_of_players("abc")

    test_player = Player("Larry Bird", 30, "playoffs")
    result_df = test_player.get_player_profile()
    statistics_per_game_basis(result_df, "GP", "MIN", "FGM", "FGA", "FG3M", "FG3A", "FTM",
                              "FTA", "OREB", "DREB", "REB", "AST", "STL", "BLK", "TOV", "PF", "PTS")
    result_df["YEAR_IN_LEAGUE"] = result_df["PLAYER_AGE"] - \
        min(result_df["PLAYER_AGE"]) + 1
    result_df["SEASON_TYPE"] = test_player.season
    result_df["PLAYER"] = test_player.name
    result_df_cleaned = result_df[["SEASON_TYPE", "PLAYER", "PLAYER_AGE", "YEAR_IN_LEAGUE", "SEASON_ID", "TEAM_ABBREVIATION", "GP", 'MIN', "MIN_PER_GAME", "FGM", "FGM_PER_GAME", "FGA", "FGA_PER_GAME", "FG_PCT", "FG3M", "FG3M_PER_GAME", "FG3A",
                                   "FG3A_PER_GAME", "FG3_PCT", "FTM", "FTM_PER_GAME", "FTA", "FTA_PER_GAME", "FT_PCT", "OREB", "OREB_PER_GAME", "DREB", "DREB_PER_GAME", "REB", "REB_PER_GAME", "AST",
                                   "AST_PER_GAME", "STL", "STL_PER_GAME", "BLK", "BLK_PER_GAME", "TOV", "TOV_PER_GAME", "PF", "PF_PER_GAME", "PTS", "PTS_PER_GAME"]]
    inputs = iter(["Larry Bird", "30", "playoffs"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert result_df_cleaned.equals(number_of_players(1)[0]) == True

    inputs = iter(["Kobe Bryant", "33", "playoffs"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert result_df_cleaned.equals(number_of_players(1)[0]) == False


def test_statistics_per_game_basis():
    test_df = pd.DataFrame([["Lebron James", 10, 400], ["Lebron James", 15, 450], [
                           "Lebron James", 6, 300]], columns=["NAME", "TOTAL_GAMES_PLAYED", "TOTAL_POINTS"])
    result_df = statistics_per_game_basis(
        test_df, "TOTAL_GAMES_PLAYED", "TOTAL_POINTS")
    answer_df = pd.DataFrame([["Lebron James", 10, 400, 40.0], ["Lebron James", 15, 450, 30.0], [
        "Lebron James", 6, 300, 50.0]], columns=["NAME", "TOTAL_GAMES_PLAYED", "TOTAL_POINTS", "TOTAL_POINTS_PER_GAME"])
    assert result_df.equals(answer_df) == True

    with pytest.raises(TypeError):
        test_df_wrong = pd.DataFrame([["Lebron James", "10", 400], ["Lebron James", 15, "450"], [
            "Lebron James", "6", "300"]], columns=["NAME", "TOTAL_GAMES_PLAYED", "TOTAL_POINTS"])
        result_df_wrong = statistics_per_game_basis(
            test_df_wrong, "TOTAL_GAMES_PLAYED", "TOTAL_POINTS")
        result_df_wrong.equals(answer_df)


def test_statistics_to_analyse_for_x_axis(monkeypatch):
    test_df = pd.DataFrame([["Lebron James", 10, 400, 200, 100], ["Lebron James", 15, 450, 250, 150], [
        "Lebron James", 6, 300, 120, 60]], columns=["NAME", "TOTAL_GAMES_PLAYED", "TOTAL_POINTS", "TOTAL_3PM", "TOTAL_FTM"])
    monkeypatch.setattr("builtins.input", lambda _: "3")
    columns_series_result = statistics_to_analyse_for_x_axis(test_df)
    assert columns_series_result == "TOTAL_3PM"
    assert columns_series_result != "TOTAL_GAMES_PLAYED"

    monkeypatch.setattr("builtins.input", lambda _: "1")
    columns_series_result = statistics_to_analyse_for_x_axis(test_df)
    assert columns_series_result == "TOTAL_GAMES_PLAYED"
    assert columns_series_result != "NAME"
