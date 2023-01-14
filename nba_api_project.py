import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
from nba_api.stats.static import players
from nba_api.stats.endpoints import playerprofilev2


# Create a Player class object with name, age (to only include up till prime years), season (Regular or Playoffs) to analyse
# User input for NBA Player Name
# Web Scrapping using a custom API: https://github.com/swar/nba_api on the official nba website: https://www.nba.com/stats
# Reference: https://medium.com/@hannaoui/how-to-get-data-of-any-nba-player-for-beginners-nba-api-80c028b57d97
# Create visualisations using matplotlib


class Player:
    def __init__(self, name="Kobe Bryant", age=35, season="regular season"):
        self.name = name
        self.age = age
        self.season = season

    def get_player_info(self):
        # valid input for player_name
        while True:
            try:
                player_id = players.find_players_by_full_name(self.name)[
                    0]["id"]
                break
            except IndexError:
                print("Invalid player name. Please try again.")
                continue
        return player_id

    def get_player_profile(self):
        # total basis by default
        player_id = self.get_player_info()

        # check if valid input for game_period, Pre Season = 8; Regular Season = 0, Playoffs = 2
        while True:
            if self.season.lower() == "pre season":
                player_profile = playerprofilev2.PlayerProfileV2(
                    player_id=player_id).get_data_frames()[8]
                break
            elif self.season.lower() == "regular season":
                player_profile = playerprofilev2.PlayerProfileV2(
                    player_id=player_id).get_data_frames()[0]
                break
            elif self.season.lower() == "playoffs":
                player_profile = playerprofilev2.PlayerProfileV2(
                    player_id=player_id).get_data_frames()[2]
                break
            else:
                continue

        # convert age column to int
        player_profile["PLAYER_AGE"] = player_profile["PLAYER_AGE"].apply(
            np.int64)

        # age filter
        player_profile_till_age = player_profile[player_profile["PLAYER_AGE"] <= self.age]
        return player_profile_till_age


# calculate how many players to analyse and store in a dataframe each. Output is a list of dataframes
def number_of_players(n):
    player_list = []
    for i in range(n):
        player_name = input("Player name: ").strip()
        player_age = int(input("Player data up till which age: ").strip())
        while True:
            season_type = input("Season type: ").strip().lower()
            if season_type not in ["pre season", "regular season", "playoffs"]:
                continue
            else:
                break
        player = Player(player_name, player_age, season_type)

        # original dataframe columns: ["PLAYER_ID", "SEASON_ID", "LEAGUE_ID", "TEAM_ID", "TEAM_ABBREVIATION",
        # "PLAYER_AGE", "GP", "GS", "MIN", "FGM", "FGA", "FG_PCT", "FG3M", "FG3A", "FG3_PCT", "FTM", "FTA", "FT_PCT",
        # "OREB", "DREB", "REB", "AST", "STL", "BLK", "TOV", "PF", "PTS"]

        # assigning each dataframe to each player object
        df = player.get_player_profile()

        # calculate per game basis
        statistics_per_game_basis(df, "GP", "MIN", "FGM", "FGA", "FG3M", "FG3A", "FTM",
                                  "FTA", "OREB", "DREB", "REB", "AST", "STL", "BLK", "TOV", "PF", "PTS")

        # convert age to nth year in league, based on what age player enters the league
        df["YEAR_IN_LEAGUE"] = df["PLAYER_AGE"] - min(df["PLAYER_AGE"]) + 1

        # add in season and player name in respective dataframe
        df["SEASON_TYPE"] = player.season
        df["PLAYER"] = player.name

        # sort order of columns
        df_cleaned = df[["SEASON_TYPE", "PLAYER", "PLAYER_AGE", "YEAR_IN_LEAGUE", "SEASON_ID", "TEAM_ABBREVIATION", "GP", 'MIN', "MIN_PER_GAME", "FGM", "FGM_PER_GAME", "FGA", "FGA_PER_GAME", "FG_PCT", "FG3M", "FG3M_PER_GAME", "FG3A",
                         "FG3A_PER_GAME", "FG3_PCT", "FTM", "FTM_PER_GAME", "FTA", "FTA_PER_GAME", "FT_PCT", "OREB", "OREB_PER_GAME", "DREB", "DREB_PER_GAME", "REB", "REB_PER_GAME", "AST",
                         "AST_PER_GAME", "STL", "STL_PER_GAME", "BLK", "BLK_PER_GAME", "TOV", "TOV_PER_GAME", "PF", "PF_PER_GAME", "PTS", "PTS_PER_GAME"]]

        # list of dataframes for each player
        player_list.append(df_cleaned)
    return player_list


def statistics_per_game_basis(df, total_games, *total_stats):
    for i in range(len(total_stats)):
        df[total_stats[i] +
            "_PER_GAME"] = (df[total_stats[i]]/df[total_games]).round(decimals=2)
    return df


# convert column names in series then ask user to input what statistic they want to analyse
def statistics_to_analyse_for_x_axis(df):
    columns_series = pd.Series(df.columns)
    print(columns_series)

    # check if valid input for statistic index
    while True:
        try:
            statistic_index = int(input(
                "What statistic do you want to analyse for x? Enter the corresponding numerical index: ").strip())
            x_statistic = columns_series[statistic_index]
            break
        except (IndexError, ValueError):
            print("Enter an appropriate number")
            continue
    return x_statistic


def statistics_to_analyse_for_y_axis(df):
    columns_series = pd.Series(df.columns)
    print(columns_series)

    # check if valid input for statistic index
    while True:
        try:
            statistic_index = int(input(
                "What statistic do you want to analyse for y? Enter the corresponding numerical index: ").strip())
            y_statistic = columns_series[statistic_index]
            break
        except (IndexError, ValueError):
            print("Enter an appropriate number")
            continue
    return y_statistic


# either pass in one value for one plot or pass in lists as arguments for multiple plots
def statistics_to_line_plot(x_column, y_column, title, x_label, y_label, df):
    plt.figure()

    # adding each player name in player_list
    # create a line plot for each dataframe in the same figure
    for i in range(len(df)):
        plt.plot(df[i][x_column], df[i][y_column], label=df[i]
                 ["PLAYER"][0] + " - " + df[i]["SEASON_TYPE"][0])
        plt.ioff()
    # layout settings of plot
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend(loc="best")
    plt.rcParams["figure.autolayout"] = True
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["top"].set_visible(False)
    return plt.show()


def statistics_to_scatter_plot(x_column, y_column, title, x_label, y_label, df):
    plt.figure()

    # adding each player name in player_list
    # create a line plot for each dataframe in the same figure
    for i in range(len(df)):
        plt.scatter(df[i][x_column], df[i][y_column], label=df[i]
                    ["PLAYER"][0] + " - " + df[i]["SEASON_TYPE"][0])
        plt.ioff()
    # layout settings of plot
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend(loc="best")
    plt.rcParams["figure.autolayout"] = True
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["top"].set_visible(False)
    return plt.show()


def main():
    player_number = int(
        input("How many players do you want to analyse? ").strip())
    number_of_df = number_of_players(player_number)

    # plot key statistics
    # generate variables required
    x_column = statistics_to_analyse_for_x_axis(number_of_df[0])
    y_column = statistics_to_analyse_for_y_axis(number_of_df[0])
    title = f"{y_column} vs {x_column}"
    x_label = x_column
    y_label = y_column
    df_list = number_of_df

    # line plot if x-axis is in ["PLAYER", "PLAYER_AGE", "YEAR_IN_LEAGUE", "SEASON_ID"]
    # if not then scatter plot
    if x_column in ["PLAYER_AGE", "YEAR_IN_LEAGUE", "SEASON_ID"]:
        statistics_to_line_plot(x_column, y_column, title,
                                x_label, y_label, df_list)
    else:
        statistics_to_scatter_plot(
            x_column, y_column, title, x_label, y_label, df_list)


if __name__ == "__main__":
    main()
