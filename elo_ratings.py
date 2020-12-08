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

#create division groupings:
divisions_dict = {"NFC_East" : ["Eagles", "Giants", "Cowboys", "Washington"],
                  "NFC North" : ["Bears","Packers","Lions","Vikings"],
                  "NFC South" : ["Buccaneers","Saints","Panthers","Falcons"],
                  "NFC West" : ["Seahawks","Cardinals","Rams","49ers"],
                  "AFC East" : ["Bills","Dolphins","Patriots","Jets"],
                  "AFC North" : ["Steelers","Ravens","Browns","Bengals"],
                  "AFC South" : ["Titans","Colts","Texans","Jaguars"],
                  "AFC West" : ["Chiefs","Raiders","Broncos","Chargers"]}

records = {"Cardinals" : [0,0,0],
           "Falcons" : [0,0,0],
           "Ravens" : [0,0,0],
           "Bills" : [0,0,0],
           "Panthers" : [0,0,0],
           "Bears" : [0,0,0],
           "Bengals" : [0,0,0],
           "Browns" : [0,0,0],
           "Cowboys" : [0,0,0],
           "Broncos" : [0,0,0],
           "Lions" : [0,0,0],
           "Packers" : [0,0,0],
           "Texans" : [0,0,0],
           "Colts" : [0,0,0],
           "Jaguars" : [0,0,0],
           "Chiefs" : [0,0,0],
           "Raiders" : [0,0,0],
           "Rams" : [0,0,0],
           "Chargers" : [0,0,0],
           "Dolphins" : [0,0,0],
           "Vikings" : [0,0,0],
           "Patriots" : [0,0,0],
           "Saints" : [0,0,0],
           "Giants" : [0,0,0],
           "Jets" : [0,0,0],
           "Eagles" : [0,0,0],
           "Steelers" : [0,0,0],
           "49ers" : [0,0,0],
           "Seahawks" : [0,0,0],
           "Buccaneers" : [0,0,0],
           "Titans" : [0,0,0],
           "Washington" : [0,0,0]}

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
        try:
            elo = data.loc[team, week]
            return elo
        except Exception:
            pass

    #set the elo for a team
    def set_elo(self, team, week, elo):
        if week != "Week 17":
            column_idx = data.columns.get_loc(week) + 1
            next_week = data.columns.values[column_idx]
            data.loc[team, next_week] = elo
        else:
            pass

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
        if team_abv == "BYE":
            pass
        else:
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

    #get teams from the division
    def get_teams_in_divsions(self, division):
        return divisions_dict[division]

    #set the average columns
    def set_average(self):
        try:
            scores.drop(columns=["Average"], axis=1)
            scores["Average"] = scores.mean(axis=1)
        except Exception:
            scores["Average"] = scores.mean(axis=1)

    #function to give a win loss or tie to a team
    def set_record(self, team, result):
        if result == 1:
            records[team][0] += 1
        elif result == -1:
            records[team][1] += 1
        else:
            records[team][2] += 1
        
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
    def adjustments(self, elo_score, home):
        if home == "H":
            elo_score += home_field_advantage
        else:
            elo_score = elo_score
        return elo_score
    
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
    def get_predicted_score(self, team, week, elo_team = 0, elo_opp = 0, plot=False, runs = 10000):
        opp = elo.get_opponent(team, week)
        if opp == "Bye":
            print("The", team, "are on a bye this week.")
        elif opp != "Bye":
            spread = self.point_spread(elo_team, elo_opp)
            if spread <= 0:
                spread = 0
            else:
                spread = spread
            score = np.random.normal(spread, standard_deviation, runs)
            avg = self.get_average_score(team)
            predicted_score = avg + score
            predicted_score = int(round(np.median(predicted_score),0))
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

    #this gets the percent chance of a team winning based on scoring
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
            if team == "Washington":
                print("Predicting", team, "will score", predicted_score, "points in", week, ".")
            elif team != "Washington":
                print("Predicting the", team, "will score", predicted_score, "points in", week, ".")
            if write == True:
                if predicted_score == "None":
                    predicted_score = "BYE"
                self.set_predicted_score(team, week, predicted_score)

    #run the game and write the predicted results into the sheet
    def get_game_and_predict_results(self, team, week, write=False, adjustments=False):
        counted_teams = []
        home_away = self.get_home_away(team, week)
        opp = elo.get_opponent(team, week)
        elo_team = elo.get_elo(team, week)
        elo_opp = elo.get_elo(opp, week)
        if adjustments == True:
            elo_team = self.adjustments(elo_team, home_away)
            elo_opp = self.adjustments(elo_opp, home_away)
        predicted_score_team = self.get_predicted_score(team, week, elo_team, elo_opp)
        predicted_score_opp = self.get_predicted_score(opp, week, elo_team, elo_opp)
        print(predicted_score_team)
        print(predicted_score_opp)
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
        #debug line
        #print(team, opp, elo_team, elo_opp, predicted_score_team, predicted_score_opp, changed_elo_home, changed_elo_away)
        if write == True:
            if week != "Week 17":
                self.set_elo(team, week, changed_elo_home)
                self.set_elo(opp, week,changed_elo_away)
                self.set_predicted_score(team, week, predicted_score_team)
                self.set_predicted_score(opp, week, predicted_score_opp)
            if week == "Week 17":
                self.set_predicted_score(team, week, predicted_score_team)
                self.set_predicted_score(opp, week, predicted_score_opp)
        return result

    #simulate the full week of scores and write to the files
    def simulate_week_and_write_to_the_data(self, week, adjustments=False, write=False):
        teams = data.index
        counted_teams = []
        for team in data.index:
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
                    elif result [2] == 0:
                        self.set_record(team, 0)
                        self.set_record(opp, 0)
                        counted_teams.append(result[0])
                        counted_teams.append(result[1])
                self.set_average()
            except Exception:
                #print("Failed for", team, "carrying elo over")
                self.set_elo(team, week, self.get_elo(team, week))

    def run_season(self, adjustments=False, write=False):
        weeks = scores.columns
        for week in weeks:
            if week != "Average":
                print(week)
                self.simulate_week_and_write_to_the_data(week, adjustments=adjustments, write=write)
            else:
                #print("Skipping column", week)
                continue                

            
#create object
elo = simulator()
#set up global data
elo.read_and_clean("D:/Elo_Ratings/elo_data.csv")
elo.read_schedule("D:/Elo_Ratings/schedule.csv")
elo.read_scores("D:/Elo_Ratings/scores.csv")
elo.set_average()
#testing code here
#elo.run_season(adjustments=True, write=True)
#elo.write_file(data,"test_elos.csv")
#elo.write_file(scores,"test_scores.csv")
#print(records)

#get scores of a specific week
#print(elo.get_game_and_predict_results("Washington", "Week 12"))
#print(elo.get_game_and_predict_results("Dallas", "Week 12"))
#print(elo.get_opponent("Dallas", "Week 12"))

elo_win = elo.get_elo("Washington", "Week 13")
elo_loss = elo.get_elo("Steelers", "Week 13")
print(elo.change_elo(elo_win, elo_loss, "A", 23, 17))

#elo.simulate_week_and_write_to_the_data("Week 2")
