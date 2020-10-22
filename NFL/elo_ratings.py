import numpy as np
import pandas as pd
from random import random

#K is the standard change per game
K = 20
home_field_advantage = 55
injuries = 10
win_streak = 10
standard_deviation = 13
team_abv = {"Cardinals" : "ARI",
            "Falcons" : "ATL",
            "Ravens" : "BAL",
            "Bills" : "BUF",
            "Panthers" : "CAR",
            "Bears" : "CHI",
            "Bengals" : "CIN",
            "Browns" : "CLE",
            "Cowboys" : "DAL",
            "Broncos" : "DEN",
            "Lions" : "DET",
            "Packers" : "GB",
            "Texans" : "HOU",
            "Colts" : "IND",
            "Jaguars" : "JAX",
            "Chiefs" : "KC",
            "Raiders" : "LV",
            "Rams" : "LAR",
            "Chargers" : "LAC",
            "Dolphins" : "MIA",
            "Vikings" : "MIN",
            "Patriots" : "NE",
            "Saints" : "NO",
            "Giants" : "NYG",
            "Jets" : "NYJ",
            "Eagles" : "PHI",
            "Steelers" : "PIT",
            "49ers" : "SF",
            "Seahawks" : "SEA",
            "Buccaneers" : "TB",
            "Titans" : "TEN",
            "Washington" : "WSH",
            "Bye" : "BYE"}

class nfl_data(object):
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

    #return the elo we are storing for now
    def get_elo(self, team, week):
        elo = data.loc[team, week]
        return elo

    #set the elo for a team
    def set_elo(self, team, week, elo):
        column_idx = data.columns.get_loc(week) + 1
        next_week = data.columns.values[column_idx]
        data.loc[team, next_week] = elo        

    #get team abreviation
    def get_abv(self, team):
        if team == "BYE":
            return "Bye"
        else:
            return team_abv[team]

    #get team from abreviation
    def get_team_abv(self, abv):
        inv_team_abv = {v: k for k, v in team_abv.items()}
        if abv.strip('@') == "BYE":
            return "Bye"
        else:
            return inv_team_abv[abv.strip('@')]

    #get home or away
    def get_home_away(self, team, week):
        team_abv = self.get_abv(team)
        opponent = schedule.loc[team_abv, week]
        if '@' in str(opponent):
            home_away = "A"
        elif '@' not in str(opponent):
            home_away =  "H"
        elif opponent == "BYE":
            home_away = "Bye"    
        return home_away
 

    #get the opponent for the week
    def get_opponent(self, team, week):
        team_abv = self.get_abv(team)
        opponent = schedule.loc[team_abv, week]
        opponent = self.get_team_abv(opponent)
        return opponent

    #get the average score of the team
    def get_average_score(self, team):
        avg_score = scores.loc[team, "Average"]
        return avg_score

    #set the predicted scores for the week
    def set_predicted_score(self, team, week, score):
        column_idx = scores.columns.get_loc(week)
        next_week = scores.columns.values[column_idx]
        scores.loc[team, next_week] = score

    #get the score of a team for a specific week
    def get_score(self, team, week):
        score = scores.loc[team, week]
        return score

    #function to write the file
    def write_file(self, dataframe, file_name):
        dataframe.to_csv(file_name)

class elo_ratings(nfl_data):
    #calculate the percentage chance a team will win
    def weight_calc(self, eloA, eloB):
        diff = eloA - eloB
        weight = 1/(10**(-diff/400)+1)
        return round(weight,4)

    #change the elo rating accordingly
    def change_elo(self, eloA, eloB, winner, pointsA, pointsB):
        if winner == "A":
            multiplier = self.mov_multiplier(eloA, eloB, winner, pointsA, pointsB)
            weight_winner = self.weight_calc(eloA, eloB)
            weight_loser = self.weight_calc(eloB, eloA)
            elo_after_winner = eloA + multiplier * (K *(1 - weight_winner))
            elo_after_loser = eloB - multiplier * (K *(1 - weight_loser))
        if winner == "B":
            multiplier = self.mov_multiplier(eloA, eloB, winner, pointsA, pointsB)
            weight_winner = self.weight_calc(eloB, eloA)
            weight_loser = self.weight_calc(eloA, eloB)
            elo_after_winner = eloB + multiplier * (K *(1 - weight_winner))
            elo_after_loser = eloA - multiplier * (K *(1 - weight_loser))
        return [elo_after_winner, elo_after_loser]

    #get the multiplier for the k value
    def mov_multiplier(self, eloA, eloB, winner, pointsA, pointsB):
        if winner == "A":
            winner_point_diff = pointsA - pointsB
            winner_elo_diff = eloA - eloB
        if winner == "B":
            winner_point_diff = pointsB - pointsA
            winner_elo_diff = eloB - eloA
        multiplier = np.log(winner_point_diff+1) * (2.2/((winner_elo_diff*.001)+2.2))
        return multiplier

    #assuming 25 elo points is one point in the NFL
    def point_spread(self, eloA, eloB):
        diff = eloA - eloB
        spread = round(diff/25,2)
        return spread

    #make adjustments #TODO
    #this part is important since it adjusts the teams to see if they have a better chance of winning or not
    def adjustments(self, elo, home):
        if home_away == "H":
            elo += home_field_advantage
        else:
            elo = elo

    #print some game details such as who's playing and the spread as well as percent chance
    def print_game_details(self, week, team):
        home_away = self.get_home_away(team, week)
        opp = elo.get_opponent(team, week)
        if opp == "Bye":
            print("The", team, "are on a bye this week.\n")
        else:
            elo_team = elo.get_elo(team, week)
            elo_opp = elo.get_elo(opp, week)
            teams_elo = {elo_team : team,
                         elo_opp : opp}
            better_team = max(elo_team, elo_opp)
            worse_team = min(elo_team, elo_opp)
            odds = self.weight_calc(better_team, worse_team)
            odds_percent = odds * 100
            spread = self.point_spread(better_team, worse_team)
            if team == "Washington" and teams_elo[better_team] == "Washington":
                print(team, "is playing the", opp, "in", week, "and are", home_away)
                print(teams_elo[better_team], "has a", odds_percent,
                        "% chance of winning, with a spread of", spread,"\n")
            elif team == "Washington" and teams_elo[better_team] != "Washington":
                print(team, "is playing the", opp, "in", week, "and are", home_away)
                print("The", teams_elo[better_team], "have a", odds_percent,
                        "% chance of winning, with a spread of", spread,"\n")
            else:
                print("The", team, "are playing the", opp, "in", week, "and are", home_away)
                print("The", teams_elo[better_team], "have a", odds_percent,
                        "% chance of winning, with a spread of", spread,"\n")

    #calculate the brier score for accuracy
    #1 for win-loss if it's right
    #0 for win_loss if it's wrong
    def brier_score(chance, odds, win_loss):
        return (odds-win_loss)**2

       #predict the scores for the team
    def get_predicted_score(self, team, week, runs = 1000, plot=False):
        opp = elo.get_opponent(team, week)
        if opp == "Bye":
            print("The", team, "are on a bye this week.")
        else:
            elo_team = elo.get_elo(team, week)
            elo_opp = elo.get_elo(opp, week)
            spread = self.point_spread(elo_team, elo_opp)
            score = np.random.normal(spread, standard_deviation, runs)
            avg = self.get_average_score(team)
            predicted_score = avg + score
            predicted_score = int(round(np.mean(predicted_score),0))
            if plot:
                _ = plt.hist(score)
                plt.show()
            return predicted_score

#simulator for each week
class simulator(elo_ratings):
    def run_week(self, week, simulate=True):
        teams = data.index
        for team in teams:
            self.print_game_details(week, team)

    def simulate_games(self, team, week, runs=100000):
        home_away = self.get_home_away(team, week)
        opp = elo.get_opponent(team, week)
        if opp == "Bye":
            print("The", team, "are on a bye this week.\n")
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
            chance = (wins/runs)*100
            if team == "Washington":
                print("Simulating for", team, "we get a winning chance of", chance,"%")
            else:
                print("Simulating for the", team, "we get a winning chance of", chance,"%")

    #calculate the scores for each game of the week
    def simulate_week_with_scores(self, week, write=False):
        teams = data.index
        for team in teams:
            predicted_score = self.get_predicted_score(team, week)
            print("Predicting the", team, "will score", predicted_score, "points in", week, ".")
            if write == True:
                if predicted_score == "None":
                    predicted_score = "BYE"
                self.set_predicted_score(team, week, predicted_score)
            
#create object
elo = simulator()
#set up global data
elo.read_and_clean("D:/Elo_Ratings/elo_data.csv")
elo.read_schedule("D:/Elo_Ratings/schedule.csv")
elo.read_scores("D:/Elo_Ratings/scores.csv")
#testing code here
#elo.run_week("Week 7")
elo.simulate_week_with_scores("Week 7", write=True))
                                       


