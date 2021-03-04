import numpy as np
import pandas as pd
from random import random

# K is the standard change per game
K = 20  # historical change from nba based of 538's data
home_field_advantage = 240/3.5
injuries = 10
win _streak = 10
# https://www.theonlycolors.com/2020/4/27/21226073/the-variance-of-college-basketball-how-big-is-it-and-where-does-it-come-from
# not sure if this is good enough, but will read more into it later
standard_deviation = 10
team_abv = {"Hawks": "ATL",
            "Nets": "BKN",
            "Celtics": "BOS",
            "Hornets": "CHA",
            "Bulls": "CHI",
            "Cavaliers": "CLE",
            "Mavericks": "DAL",
            "Nuggets": "DEN",
            "Pistons": "DET",
            "Warriors": "GSW",
            "Rockets": "HOU",
            "Pacers": "IND",
            "Clippers": "LAC",
            "Lakers": "LAL",
            "Grizzlies": "MEM",
            "Heat": "MIA",
            "Bucks": "MIL",
            "Timberwolves": "MIN",
            "Pelicans": "NOP",
            "Knicks": "NYK",
            "Thunder": "OKC",
            "Magic": "ORL",
            "76ers": "PHI",
            "Suns": "PHX",
            "Trail Blazers": "POR",
            "Kings": "SAC",
            "Spurs": "SAS",
            "Raptors": "TOR",
            "Jazz": "UTA",
            "Wizards": "WAS",
            "Bye": "BYE"}

# create division groupings:
divisions_dict = {"Eastern Conference": ["76ers", "Nets", "Bucks", "Celtics", "Raptors",
                                         "Knicks", "Heat", "Hornets", "Pacers", "Bulls",
                                         "Hawks", "Cavaliers", "Wizards", "Magic", "Pistons"],
                  "Western Conference": ["Jazz", "Suns", "Lakers", "Clippers", "Spurs",
                                         "Trail Blazers", "Nuggets", "Warriors", "Grizzlies",
                                         "Mavericks", "Pelicans", "Thunder", "Kings", "Rockets",
                                         "Timberwolves"]}

records = {"Hawks": [0, 0],
           "Nets": [0, 0],
           "Celtics": [0, 0],
           "Hornets": [0, 0],
           "Bulls": [0, 0],
           "Cavaliers": [0, 0],
           "Mavericks": [0, 0],
           "Nuggets": [0, 0],
           "Pistons": [0, 0],
           "Warriors": [0, 0],
           "Rockets": [0, 0],
           "Pacers": [0, 0],
           "Clippers": [0, 0],
           "Lakers": [0, 0],
           "Grizzlies": [0, 0],
           "Heat": [0, 0],
           "Bucks": [0, 0],
           "Timberwolves": [0, 0],
           "Pelicans": [0, 0],
           "Knicks": [0, 0],
           "Thunder": [0, 0],
           "Magic": [0, 0],
           "76ers": [0, 0],
           "Suns": [0, 0],
           "Trail Blazers": [0, 0],
           "Kings": [0, 0],
           "Spurs": [0, 0],
           "Raptors": [0, 0],
           "Jazz": [0, 0],
           "Wizards": [0, 0]}


class NflData(object):
    def read_and_clean(self, file):
        global data
        data = pd.read_csv(file)
        data = data.set_index("Team/Elo")
        data = data.fillna(0)

    def read_schedule(self, file):
        global schedule
        schedule = pd.read_csv(file)
        schedule = schedule.set_index("TEAM")

    def read_scores(self, file):
        global scores
        scores = pd.read_csv(file)
        scores = scores.set_index("Teams")

    # return the elo we are storing for now
    def get_elo(self, team, week):
        try:
            elo = data.loc[team, week]
            return elo
        except Exception:
            pass

    # set the elo for a team
    def set_elo(self, team, week, elo_assigned):
        if week != "Week 17":
            column_idx = data.columns.get_loc(week) + 1
            next_week = data.columns.values[column_idx]
            data.loc[team, next_week] = elo_assigned
        else:
            pass

    # get team abbreviation
    def get_abv(self, team):
        if team == "BYE":
            return "Bye"
        else:
            return team_abv[team]

    # get team from abbreviation
    def get_team_abv(self, abv):
        inv_team_abv = {v: k for k, v in team_abv.items()}
        if abv.strip('@') == "BYE":
            return "Bye"
        else:
            return inv_team_abv[abv.strip('@')]

    # get home or away
    def get_home_away(self, team, week):
        team_abv = self.get_abv(team)
        home_away = ''
        opponent = schedule.loc[team_abv, week]
        if '@' in str(opponent):
            home_away = "A"
        elif '@' not in str(opponent):
            home_away = "H"
        elif opponent == "BYE":
            home_away = "Bye"
        return home_away

    # get the opponent for the week
    def get_opponent(self, team, week):
        team_abv = self.get_abv(team)
        if team_abv == "BYE":
            pass
        else:
            opponent = schedule.loc[team_abv, week]
            opponent = self.get_team_abv(opponent)
            return opponent

    # get the average score of the team
    def get_average_score(self, team):
        avg_score = scores.loc[team, "Average"]
        return avg_score

    # set the predicted scores for the week
    def set_predicted_score(self, team, week, score):
        column_idx = scores.columns.get_loc(week)
        next_week = scores.columns.values[column_idx]
        scores.loc[team, next_week] = score

    # get the score of a team for a specific week
    def get_score(self, team, week):
        score = scores.loc[team, week]
        return score

    # function to write the file
    def write_file(self, dataframe, file_name):
        dataframe.to_csv(file_name)

    # get teams from the divisions
    def get_teams_in_divisions(self, division):
        return divisions_dict[division]

    # set the average columns
    def set_average(self):
        try:
            scores.drop(columns=["Average"], axis=1)
            scores["Average"] = scores.mean(axis=1)
        except Exception:
            scores["Average"] = scores.mean(axis=1)

    # function to give a win loss or tie to a team
    def set_record(self, team, result):
        if result == 1:
            records[team][0] += 1
        elif result == -1:
            records[team][1] += 1
        else:
            records[team][2] += 1


class EloRatings(NflData):
    # calculate the percentage chance a team will win
    def weight_calc(self, elo_a, elo_b):
        diff = elo_a - elo_b
        weight = 1 / (10 ** (-diff / 400) + 1)
        return round(weight, 4)

    # change the elo rating accordingly
    def change_elo(self, elo_a, elo_b, winner, points_a, points_b):
        elo_after_winner = 0
        elo_after_loser = 0
        if winner == "A":
            multiplier = self.mov_multiplier(elo_a, elo_b, winner, points_a, points_b)
            weight_winner = self.weight_calc(elo_a, elo_b)
            weight_loser = self.weight_calc(elo_b, elo_a)
            elo_after_winner = elo_a + multiplier * (K * (1 - weight_winner))
            elo_after_loser = elo_b - multiplier * (K * (1 - weight_loser))
        if winner == "B":
            multiplier = self.mov_multiplier(elo_a, elo_b, winner, points_a, points_b)
            weight_winner = self.weight_calc(elo_b, elo_a)
            weight_loser = self.weight_calc(elo_a, elo_b)
            elo_after_winner = elo_b + multiplier * (K * (1 - weight_winner))
            elo_after_loser = elo_a - multiplier * (K * (1 - weight_loser))
        return [elo_after_winner, elo_after_loser]

    # get the multiplier for the k value
    def mov_multiplier(self, elo_a, elo_b, winner, points_a, points_b):
        winner_point_diff = 0
        winner_elo_diff = 0
        if winner == "A":
            winner_point_diff = points_a - points_b
            winner_elo_diff = elo_a - elo_b
        if winner == "B":
            winner_point_diff = points_b - points_a
            winner_elo_diff = elo_b - elo_a
        multiplier = np.log(winner_point_diff + 1) * (2.2 / ((winner_elo_diff * .001) + 2.2))
        return multiplier

    # assuming 3.5 points in nba is worth 100 points
    def point_spread(self, elo_a, elo_b):
        diff = elo_a - elo_b
        spread = round(diff / (100/3.5), 2)
        return spread

    # make adjustments
    # this part is important since it adjusts the teams to see if they have a better chance of winning or not
    def adjustments(self, elo_score, home):
        if home == "H":
            elo_score += home_field_advantage
        else:
            elo_score = elo_score
        return elo_score

    # print some game details such as who's playing and the spread as well as percent chance
    def print_game_details(self, week, team):
        home_away = self.get_home_away(team, week)
        opp = elo.get_opponent(team, week)
        if opp == "Bye":
            print("The", team, "are on a bye this week.\n")
        else:
            elo_team = elo.get_elo(team, week)
            elo_opp = elo.get_elo(opp, week)
            teams_elo = {elo_team: team,
                         elo_opp: opp}
            better_team = max(elo_team, elo_opp)
            worse_team = min(elo_team, elo_opp)
            odds = self.weight_calc(better_team, worse_team)
            odds_percent = odds * 100
            spread = self.point_spread(better_team, worse_team)
            print("The", team, "are playing the", opp, "in", week, "and are", home_away)
            print("The", teams_elo[better_team], "have a", odds_percent,
                  "% chance of winning, with a spread of", spread, "\n")

    # calculate the brier score for accuracy
    # 1 for win-loss if it's right
    # 0 for win_loss if it's wrong
    def brier_score(self, odds, win_loss):
        return (odds - win_loss) ** 2

    # predict the scores for the team
    def get_predicted_score(self, team, week, elo_team=0, elo_opp=0, runs=10000):
        predicted_score = 0
        opp = elo.get_opponent(team, week)
        if opp == "Bye":
            print("The", team, "are on a bye today.")
        elif opp != "Bye":
            spread = self.point_spread(elo_team, elo_opp)
            if spread <= 0:
                spread = 0
            else:
                spread = spread
            score = np.random.normal(spread, standard_deviation, runs)
            avg = self.get_average_score(team)
            predicted_score = avg + score
            predicted_score = round(np.mean(predicted_score), 2)
        return predicted_score


# simulator for each week
class Simulator(EloRatings):
    def run_week(self, week):
        teams = data.index
        for team in teams:
            self.print_game_details(week, team)

    # this gets the percent chance of a team winning based on scoring
    def simulate_games(self, team, week, runs=100000):
        opp = elo.get_opponent(team, week)
        if opp == "Bye":
            print("The", team, "are on a bye today.\n")
        else:
            elo_team = elo.get_elo(team, week)
            elo_opp = elo.get_elo(opp, week)
            odds = self.weight_calc(elo_team, elo_opp)
            wins = 0
            losses = 0
            for i in range(runs):
                result = random()
                if result <= odds:
                    wins += 1
                else:
                    losses += 1
            chance = (wins / runs) * 100
            print("Simulating for the", team, "we get a winning chance of", chance, "%")

    # calculate the scores for each game of the week
    def simulate_week_with_scores(self, week, write=False):
        teams = data.index
        for team in teams:
            predicted_score = self.get_predicted_score(team, week)
            print("Predicting the", team, "will score", predicted_score, "points in", week, ".")
            if write:
                if predicted_score == "None":
                    predicted_score = "BYE"
                self.set_predicted_score(team, week, predicted_score)

    # run the game and write the predicted results into the sheet
    def get_game_and_predict_results(self, team, week, write=False, adjustments=False):
        # counted_teams = []
        changed_elo_home = 0
        changed_elo_away = 0
        result = [0, 0, 0]
        home_away = self.get_home_away(team, week)
        opp = elo.get_opponent(team, week)
        elo_team = elo.get_elo(team, week)
        elo_opp = elo.get_elo(opp, week)
        if adjustments:
            elo_team = self.adjustments(elo_team, home_away)
            elo_opp = self.adjustments(elo_opp, home_away)
        predicted_score_team = self.get_predicted_score(team, week, elo_team, elo_opp)
        predicted_score_opp = self.get_predicted_score(opp, week, elo_opp, elo_team)
        # print(predicted_score_team)
        # print(predicted_score_opp)
        if predicted_score_team > predicted_score_opp:
            winner = "A"
            new_elos = self.change_elo(elo_team, elo_opp, winner, predicted_score_team, predicted_score_opp)
            changed_elo_home = new_elos[0]
            changed_elo_away = new_elos[1]
            result = [team, opp, 1]
        elif predicted_score_team < predicted_score_opp:
            winner = "B"
            new_elos = self.change_elo(elo_team, elo_opp, winner, predicted_score_team, predicted_score_opp)
            changed_elo_home = new_elos[1]
            changed_elo_away = new_elos[0]
            result = [team, opp, -1]
        elif predicted_score_team == predicted_score_opp:
            winner = "A"
            new_elos = self.change_elo(elo_team, elo_opp, winner, predicted_score_team, predicted_score_opp)
            changed_elo_home = new_elos[0]
            changed_elo_away = new_elos[1]
            result = [team, opp, 0]
        # debug line
        # print(team, opp, elo_team, elo_opp, predicted_score_team, predicted_score_opp,
        #       changed_elo_home, changed_elo_away)
        if write:
            if week != "Week 17":
                self.set_elo(team, week, changed_elo_home)
                self.set_elo(opp, week, changed_elo_away)
                self.set_predicted_score(team, week, predicted_score_team)
                self.set_predicted_score(opp, week, predicted_score_opp)
            if week == "Week 17":
                self.set_predicted_score(team, week, predicted_score_team)
                self.set_predicted_score(opp, week, predicted_score_opp)
        return result

    # simulate the full week of scores and write to the files
    def simulate_week_and_write_to_the_data(self, week, adjustments=False, write=False):
        teams = data.index
        counted_teams = []
        for team in teams:
            opp = self.get_opponent(team, week)
            try:
                result = self.get_game_and_predict_results(team, week, adjustments=adjustments, write=write)
                if result[0] not in counted_teams and result[1] not in counted_teams:
                    if result[2] == 1:
                        self.set_record(team, 1)
                        self.set_record(opp, -1)
                        counted_teams.append(result[0])
                        counted_teams.append(result[1])
                    elif result[2] == -1:
                        self.set_record(team, -1)
                        self.set_record(opp, 1)
                        counted_teams.append(result[0])
                        counted_teams.append(result[1])
                    elif result[2] == 0:
                        self.set_record(team, 0)
                        self.set_record(opp, 0)
                        counted_teams.append(result[0])
                        counted_teams.append(result[1])
                self.set_average()
            except Exception:
                # print("Failed for", team, "carrying elo over")
                self.set_elo(team, week, self.get_elo(team, week))

    def run_season(self, adjustments=False, write=False):
        weeks = scores.columns
        for week in weeks:
            if week != "Average":
                print(week)
                self.simulate_week_and_write_to_the_data(week, adjustments=adjustments, write=write)
            else:
                # print("Skipping column", week)
                continue

    def final_standings(self, records):
        for x in records:
            total_score = 0
            total_score += records[x][0]
            total_score += (records[x][2] / 2)
            print(x, total_score)


# create object
elo = Simulator()
# set up global data
elo.read_and_clean("D:/Elo_Ratings/elo_data.csv")
elo.read_schedule("D:/Elo_Ratings/schedule.csv")
elo.read_scores("D:/Elo_Ratings/scores.csv")
elo.set_average()
# testing code here
elo.run_season(adjustments=True, write=True)
# elo.write_file(data,"test_elos.csv")
# elo.write_file(scores,"test_scores.csv")
print(records)
elo.final_standings(records)

# get scores of a specific week
# print(elo.get_game_and_predict_results("Rams", "Week 15"))
# print(elo.get_game_and_predict_results("Chargers", "Week 15"))

# elo_win = elo.get_elo("Ravens", "Week 14")
# elo_loss = elo.get_elo("Browns", "Week 14")
# print(elo.change_elo(elo_win, elo_loss, "A", 47, 42))

# elo.simulate_week_and_write_to_the_data("Week 2")