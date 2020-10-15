import numpy as np
import pandas as pd
import os

#K is the standard change per game
K = 20
home_field_advantage = 55
injuries = 10
win_streak = 10
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
            "Washington" : "WSH"}

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

    #return the elo we are storing for now
    def get_elo(self, team, week):
        elo = data.loc[team, week]
        return elo

    #get team abreviation
    def get_abv(self, team):
        return team_abv[team]

    #get team from abreviation
    def get_team_abv(self, abv):
        inv_team_abv = {v: k for k, v in team_abv.items()}
        return inv_team_abv[abv.strip('@')]

    #get home or away
    def get_home_away(self, team, week):
        team_abv = self.get_abv(team)
        opponent = schedule.loc[team_abv, week]
        if '@' in str(opponent):
            home_away = "A"
        else:
            home_away =  "H"
        return home_away

    #get the opponent for the week
    def get_opponent(self, team, week):
        team_abv = self.get_abv(team)
        opponent = schedule.loc[team_abv, week]
        opponent = self.get_team_abv(opponent)
        return opponent

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

    #make adjustments
    def adjustments(self, elo, home):
        if home_away == "H":
            elo += home_field_advantage
        else:
            elo = elo

#create object
elo = elo_ratings()
#set up global data
elo.read_and_clean("D:/Elo_Ratings/elo_data.csv")
elo.read_schedule("D:/Elo_Ratings/schedule.csv")
#testing code here
#quickly automate one search
week = "Week 2"
team = "Eagles"
home_away = elo.get_home_away(team, week)
opp = elo.get_opponent(team, week)
elo_team = elo.get_elo(team, week)
elo_opp = elo.get_elo(opp, week)
print("The", team, "week 2 are playing the", opp)
print("The", team, "are", home_away, "this week!")
print("The", team, "have an elo of", elo_team)
print("The" ,opp, "have an elo of", elo_opp)
spread = elo.point_spread(max(elo_team, elo_opp), min(elo_team, elo_opp))
print("We are predicting a spread of -", spread, "in favor of the higher elo team")
