# By: Benjamin Goebel
# Date: August 24th, 2017
# Description: This program analyzes and graphs the 2016 MLB batting data.
#              I consulted source #1 (see ReadMe for details)for general help
#              on this program.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class BaseballAnalytics(object):

    # Purpose: Initializes all class variables.
    # Arguments: None.
    # Returns: Nothing.
    def __init__(self):
        stats_file = pd.ExcelFile('mlb-stats2016.xlsx')
        self.__batter_stats = stats_file.parse('Batters')
        self.__batter_stats.index = self.__batter_stats['PLAYER']
        self.__batter_stats = self.__batter_stats.drop('PLAYER', axis = 1)
        self.__batter_stats.index = self.__batter_stats.index.map(str.title)
        standings = {"arizona diamondbacks": (69, 93), \
                     "atlanta braves": (68, 93), \
                     "baltimore orioles": (89, 73), \
                     "boston red sox": (93, 69), \
                     "chicago cubs": (103, 58), \
                     "chicago white sox": (78, 84), \
                     "cincinnati reds": (68, 94), \
                     "cleveland indians": (94, 67), \
                     "colorado rockies": (75, 87), \
                     "detroit tigers": (86, 75), \
                     "miami marlins": (79, 82), \
                     "houston astros": (84, 78), \
                     "kansas city royals": (81, 81), \
                     "los angeles angels": (74, 88), \
                     "los angeles dodgers": (91, 71), \
                     "milwaukee brewers": (73, 89), \
                     "minnesota twins": (59, 103), \
                     "new york yankees": (84, 78), \
                     "new york mets": (87, 75), \
                     "oakland athletics": (69, 93), \
                     "philadelphia phillies": (71, 91), \
                     "pittsburgh pirates": (78, 83), \
                     "san diego padres": (68, 94), \
                     "san francisco giants": (87, 75), \
                     "seattle mariners": (86, 76), \
                     "st. louis cardinals": (86, 76), \
                     "tampa bay rays": (68, 94), \
                     "texas rangers": (95, 67), \
                     "toronto blue jays": (89, 73), \
                     "washington nationals": (95, 67)}
        self.__standings_frame = pd.DataFrame(standings).T
        self.__standings_frame.columns = ['Wins', 'Losses']
        winning_pct = pd.Series(self.__standings_frame['Wins']/ \
                                  (self.__standings_frame['Wins'] + \
                                   self.__standings_frame['Losses']), \
                                   index = self.__standings_frame.index)
        self.__standings_frame = self.__standings_frame.assign(Winning_Pct = \
                                                               winning_pct)
        self.__standings_frame.sort_values(by= 'Winning_Pct', \
                                           ascending = False, inplace = True)
        rankings = pd.Series(range(1, 31), index = self.__standings_frame.index)
        self.__standings_frame = self.__standings_frame.assign(Rankings = \
                                                               rankings)
        self.__standings_frame = self.__standings_frame.reset_index()
        self.__standings_frame = self.__standings_frame.set_index('Rankings')
        self.__standings_frame.columns = ['Team', 'Wins', 'Losses', \
                                          'Winning Pct']
        self.__standings_frame['Team'] = \
        self.__standings_frame['Team'].map(str.title)

    # Purpose: Checks if a string is a valid stat.
    # Arguments: A string: the stat to be verified.
    # Returns: A boolean: True if the stat passed to the function is a valid
    #          stat and False if otherwise.
    def is_in_stats(self, stat):
        stats = ['G', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI', 'BB', 'K', \
                 'SB', 'CS', 'AVG', 'SLG', 'OBP', 'OPS']
        return stat in stats

    # Purpose: Converts a baseball team's name to the team name's abbreviation.
    # Arguments: A string: the team name.
    # Returns: A string: the team name's abbreviation.
    def name_to_abbrev(self, team):
        team = team.lower()
        team_abbreviations = {"arizona diamondbacks": "AZ", \
                              "atlanta braves": "ATL", \
                              "baltimore orioles": "BAL", \
                              "boston red sox": "BOS", \
                              "chicago cubs": "CHC", \
                              "chicago white sox": "CHW", \
                              "cincinnati reds": "CIN", \
                              "cleveland indians": "CLE", \
                              "colorado rockies": "COL", \
                              "detroit tigers": "DET", \
                              "miami marlins": "MIA", \
                              "houston astros": "HOU", \
                              "kansas city royals": "KC", \
                              "los angeles angels": "LAA",
                              "los angeles dodgers": "LAD", \
                              "milwaukee brewers": "MIL", \
                              "minnesota twins": "MIN", \
                              "new york yankees": "NYY", \
                              "new york mets": "NYM", \
                              "oakland athletics": "OAK", \
                              "philadelphia phillies": "PHI", \
                              "pittsburgh pirates": "PIT", \
                              "san diego padres": "SD", \
                              "san francisco giants": "SF", \
                              "seattle mariners": "SEA", \
                              "st. louis cardinals": "STL", \
                              "tampa bay rays": "TB", \
                              "texas rangers": "TEX", \
                              "toronto blue jays": "TOR", \
                              "washington nationals": "WSH"}
        return team_abbreviations[team]

    # Purpose: Gets the 2016 MLB standings.
    # Arguments: None.
    # Returns: A DataFrame: the 2016 MLB standings.
    def get_standings(self):
        return self.__standings_frame

    # Purpose: Gets a specified 2016 MLB roster.
    # Arguments: A string: the team name's abbreviation
    # Returns: A DataFrame: the players on the team
    def get_team_roster(self, team_abbrev):
        return self.__batter_stats[self.__batter_stats['Team'] == team_abbrev]

    # Purpose: Gets a specified 2016 MLB player's season stats.
    # Arguments: Two string: the player's first and last name.
    # Returns: A DataFrame: the specified MLB player's season stats.
    def get_player_stats(self, lastn, firstn):
        playern = lastn + ", " + firstn
        playern = playern.title()
        return self.__batter_stats.ix[playern]

    # Purpose: For each 2016 MLB team, this function averages the players'
    #          stats.
    # Arguments: None.
    # Returns: A DataFrame: The means of each team's stats.
    def get_avg_team_stats(self):
        no_fas = self.__batter_stats[self.__batter_stats['Team'] != 'FA']
        return no_fas.groupby(no_fas['Team']).mean().round(3)

    # Purpose: For each 2016 MLB team, this function takes the median of the
    #          players' stats.
    # Arguments: None.
    # Returns: A DataFrame: The medians of each team's stats.
    def get_med_team_stats(self):
        no_fas = self.__batter_stats[self.__batter_stats['Team'] != 'FA']
        return no_fas.groupby(no_fas['Team']).median()

    # Purpose: For each 2016 MLB team, this function takes the standard
    #          deviation of the players' stats.
    # Arguments: None.
    # Returns: A DataFrame: The standard deviations of each team's stats.
    def get_std_team_stats(self):
        no_fas = self.__batter_stats[self.__batter_stats['Team'] != 'FA']
        return no_fas.groupby(no_fas['Team']).std().round(3)

    # Purpose: Gets the mean of the specified stat for all 2016 MLB players.
    # Arguments: A string: the stat.
    # Returns: A float: the mean.
    def get_mean_stat(self, stat):
        return round(self.__batter_stats[stat].mean(), 3)

    # Purpose: Gets the median of the specified stat for all 2016 MLB players.
    # Arguments: A string: the stat.
    # Returns: A float: the median.
    def get_median_stat(self, stat):
        return self.__batter_stats[stat].median()

    # Purpose: Gets the standard deviation of the specified stat for all
    #          2016 MLB players.
    # Arguments: A string: the stat.
    # Returns: A float: the standard deviation.
    def get_std_stat(self, stat):
        return round(self.__batter_stats[stat].std(), 3)

    # Purpose: Gets the player with the max score for the specified stat.
    # Arguments: A string: the stat.
    # Returns: A Series: The name of the player with the player's corresponding
    #          score for the specified stat.
    def get_max_stat_player(self, stat):
        return self.__batter_stats[self.__batter_stats[stat] == \
                                   self.__batter_stats[stat].max()][stat]

    # Purpose: Gets the players in the 2016 MLB in the specified percentile
    #          or in a percentile that is greater than the specified percentile
    #          of the specified stat.
    # Arguments: A string: the stat. A float: the quantile.
    # Returns: A Series: the players and their corresponding
    #          scores for the specified stat.
    def get_quantile_stat(self, stat, quantile):
        players = self.__batter_stats[self.__batter_stats[stat] >= \
                  self.__batter_stats[stat].quantile(quantile)]
        return players[stat].sort_values(ascending = True)

    # Purpose: Gets the specified MLB player's percentile for each stat.
    # Arguments: Two strings: the player's first and last name.
    # Returns: A dictionary of each stat with its corresponding percentile.
    def get_player_quantile(self, lastn, firstn):
        lastn = lastn.capitalize()
        firstn = firstn.capitalize()
        original_playern = lastn + ", " + firstn
        num_players = float(len(self.__batter_stats))
        quantiles = {'G': '',
                     'AB': '',
                     'R': '',
                     'H': '',
                     '2B': '',
                     '3B': '',
                     'HR': '',
                     'RBI': '',
                     'BB': '',
                     'K': '',
                     'SB': '',
                     'CS': '',
                     'AVG': '',
                     'SLG': '',
                     'OBP': '',
                     'OPS': ''}
        for stat in quantiles.keys():
            players_by_stat = self.__batter_stats.sort_values(by=stat)
            playern = players_by_stat[players_by_stat[stat] ==
                                      self.__batter_stats.ix[original_playern, \
                                                      stat]].ix[0].name
            quantiles[stat] = str(round((100 * int(\
                                         players_by_stat.index.get_loc(playern)\
                                         + 1) / num_players), 1)) + '%'
        print("Name: " + original_playern)
        for stat in quantiles.keys():
            print(stat + ': ' + quantiles[stat])

    # Purpose: Creates a horizontal bar graph with each team on the y-axis
    #          and each team's total specified stat on the x-axis.
    # Arguments: A string: the specified stat.
    # Returns: Nothing.
    def graph_team_by_stat(self, stat):
        stat = stat.upper()
        no_fa = self.__batter_stats[self.__batter_stats['Team'] != 'FA']
        grouped_by_teams = no_fa.groupby(no_fa['Team'])
        grouped_by_teams[stat].sum().sort_values(ascending = True).plot.barh()
        plt.xlabel(stat)
        plt.ylabel('Team')
        plt.title(("%s By Team") % (stat))
        plt.show()

    # Purpose: Creates a scatter plot comparing two 2016 MLB stats. The first
    #          stat corresponds to the x-axis, and the second stat corresponds
    #          to the y-axis.
    # Arguments: Two strings: the two stats.
    # Returns: Nothing.
    def graph_stat_by_stat(self, stat1, stat2):
        stat1 = stat1.upper()
        stat2 = stat2.upper()
        plt.scatter(self.__batter_stats[stat1], self.__batter_stats[stat2])
        plt.xlabel(stat1)
        plt.ylabel(stat2)
        plt.title(("%s versus %s") % (stat2, stat1))
        plt.show()

    # Purpose: Graphs a bar graph with 2 bars per stat, comparing two specified
    #          teams in each stat, respectively.
    # Arguments: Two strings: the two baseball teams' abbreviations.
    # Returns: Nothing.
    # Sources: I consulted source # 2 for help on
    #          graphing multiple bars (see ReadMe for details)
    def graph_team_comparison(self, team_abbrev1, team_abbrev2):
        team1 = \
        self.__batter_stats[self.__batter_stats['Team'] == team_abbrev1]
        team1_edit = team1.drop(['POS', 'Team', 'CS', 'AVG', 'SLG', 'OBP', \
                                 'OPS'], axis = 1)
        team1_edit_summed = team1_edit.sum()
        length = np.arange(team1_edit_summed.size)
        first = plt.bar(length, team1_edit_summed, color = 'b', width = 0.34)
        team2 = \
        self.__batter_stats[self.__batter_stats['Team'] == team_abbrev2]
        team2_edit = team2.drop(['POS', 'Team', 'CS', 'AVG', 'SLG', 'OBP', \
                                 'OPS'], axis = 1)
        team2_edit_summed = team2_edit.sum()
        second = plt.bar(length + 0.34, team2_edit_summed, color = 'g', \
                         width = 0.34)
        plt.xticks(length + 0.17, team2_edit_summed.index)
        plt.xlabel('Stats')
        plt.ylabel('Scores in Each Stat')
        plt.title(("A Comparison Between %s and %s in Each Stat") % \
                                     (team_abbrev1, team_abbrev2))
        plt.legend([first, second], [team_abbrev1, team_abbrev2])
        plt.show()

# Purpose: Runs and controls the BaseballAnalytics program.
# Arguments: None.
# Returns: Nothing.
def main():
    ba = BaseballAnalytics()
    command = input("Greetings, this program analyzes and graphs 2016 " + \
          "MLB Data. Enter one of the following commands: 'Get-Standings'," + \
          " 'Get-Roster', 'Get-Player-Stats', 'Get-Avg-Team-Stats'," + \
          " 'Get-Med-Team-Stats', 'Get-Std-Team-Stats',"  + \
          " 'Get-Mean-Stat', 'Get-Median-Stat', 'Get-Std-Stat'," + \
          " 'Get-Max-Stat-Player', 'Get-Quantile-Stat'," + \
          " 'Get-Player-Quantile', 'Graph-Team-By-Stat'," + \
          " 'Graph-Stat-By-Stat', 'Graph-Team-Comparison', or" + \
          " 'List-Of-Commands': ")
    command = command.lower()
    while command != 'end':
        if command == "get-standings":
            print(ba.get_standings())
        elif command == "get-roster":
            team_name = input("Enter a team name: ")
            try:
                team_abbrev = ba.name_to_abbrev(team_name)
                print(ba.get_team_roster(team_abbrev))
            except:
                print("Invalid Team Name")
        elif command == "get-player-stats":
            lastn = input("Input player's last name: ")
            firstn = input("Input player's first name: ")
            try:
                print(ba.get_player_stats(lastn, firstn))
            except:
                print("Invalid Player Name")
        elif command == "get-avg-team-stats":
            print(ba.get_avg_team_stats())
        elif command == "get-med-team-stats":
            print(ba.get_med_team_stats())
        elif command == "get-std-team-stats":
            print(ba.get_std_team_stats())
        elif command == "get-mean-stat":
            stat = input("Enter a stat (G, AB, R, H, 2B, 3B, HR, RBI, " + \
                         "BB, K, SB, CS, AVG, SLG, OBP, OPS): ")
            try:
                mean = ba.get_mean_stat(stat.upper())
                print(("The mean %s is: %.3f") % (stat.upper(), mean))
            except:
                print("Invalid Stat")
        elif command == "get-median-stat":
            stat = input("Enter a stat (G, AB, R, H, 2B, 3B, HR, RBI, " + \
                         "BB, K, SB, CS, AVG, SLG, OBP, OPS): ")
            try:
                median = ba.get_median_stat(stat.upper())
                print(("The median %s is: %.3f") % (stat.upper(), median))
            except:
                print("Invalid Stat")
        elif command == "get-std-stat":
            stat = input("Enter a stat (G, AB, R, H, 2B, 3B, HR, RBI, " + \
                         "BB, K, SB, CS, AVG, SLG, OBP, OPS): ")
            try:
                std = ba.get_std_stat(stat.upper())
                print(("The standard deviation of %s is: %.3f") % \
                      (stat.upper(), std))
            except:
                print("Invalid Stat")
        elif command == "get-max-stat-player":
            stat = input("Enter a stat (G, AB, R, H, 2B, 3B, HR, RBI, " + \
                         "BB, K, SB, CS, AVG, SLG, OBP, OPS): ")
            try:
                print(ba.get_max_stat_player(stat.upper()))
            except:
                print("Invalid Stat")
        elif command == "get-quantile-stat":
            stat = input("Enter a stat (G, AB, R, H, 2B, 3B, HR, RBI, " + \
                         "BB, K, SB, CS, AVG, SLG, OBP, OPS): ")
            stat = stat.upper()
            if not (ba.is_in_stats(stat)):
                print("Invalid Stat")
            else:
                quantile = float(input("Enter a quantile (between 0 and 1 " + \
                                       "inclusive): "))
                if quantile < 0 or quantile > 1:
                    print("Invalid Quantile")
                else:
                    print(ba.get_quantile_stat(stat, quantile))
        elif command == "get-player-quantile":
            lastn = input("Input player's last name: ")
            firstn = input("Input player's first name: ")
            try:
                ba.get_player_quantile(lastn, firstn)
            except:
                print("Invalid Player")
        elif command == "graph-team-by-stat":
            stat = input("Enter a stat (G, AB, R, H, 2B, 3B, HR, RBI, " + \
                         "BB, K, SB, CS, AVG, SLG, OBP, OPS): ")
            try:
                ba.graph_team_by_stat(stat)
            except:
                print("Invalid Stat")
        elif command == "graph-stat-by-stat":
            stat1 = input("Enter a stat (G, AB, R, H, 2B, 3B, HR, RBI, " + \
                         "BB, K, SB, CS, AVG, SLG, OBP, OPS): ")
            stat2 = input("Enter a stat (G, AB, R, H, 2B, 3B, HR, RBI, " + \
                         "BB, K, SB, CS, AVG, SLG, OBP, OPS): ")
            try:
                ba.graph_stat_by_stat(stat1, stat2)
            except:
                print("Invalid Stat(s)")
        elif command == "graph-team-comparison":
            team_name1 = input("Enter first team name: ")
            team_name2 = input("Enter second team name: ")
            try:
                team_abbrev1 = ba.name_to_abbrev(team_name1)
                team_abbrev2 = ba.name_to_abbrev(team_name2)
                ba.graph_team_comparison(team_abbrev1, team_abbrev2)
            except:
                print("Invalid Team Name(s)")
        elif command == "list-of-commands":
            print("Here is a list of the program commands: \n" + \
                  " 'Get-Standings' \n" + \
                  " 'Get-Roster' \n" + \
                  " 'Get-Player-Stats' \n" + \
                  " 'Get-Avg-Team-Stats' \n" + \
                  " 'Get-Med-Team-Stats' \n" + \
                  " 'Get-Std-Team-Stats' \n" + \
                  " 'Get-Mean-Stat' \n" + \
                  " 'Get-Median-Stat' \n" + \
                  " 'Get-Std-Stat' \n" + \
                  " 'Get-Max-Stat-Player' \n" + \
                  " 'Get-Quantile-Stat' \n" + \
                  " 'Get-Player-Quantile' \n" + \
                  " 'Graph-Team-By-Stat' \n" + \
                  " 'Graph-Stat-By-Stat' \n" + \
                  " 'Graph-Team-Comparison' \n" + \
                  " 'List-Of-Commands' ")
        else:
            print("Invalid Command")
        command = input("Enter a command: ")
        command = command.lower()

main()
