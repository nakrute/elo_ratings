import numpy as np
import pandas as pd

#K is the standard change per game
K = 20
home_field_advantage = 55
injuries = 10
win_streak = 10

class nfl_data(object):
    def read_and_clean(self, file):
        pass

class elo_ratings(object):
    #return the elo we are storing for now
    def get_elo(self, team):
        pass
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

    #this needs to go into the change_elo function
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

    #assuming 65 elo points is one point in the NFL
    def point_spread(self, eloA, eloB):
        diff = eloA - eloB
        spread = round(diff/65,2)
        return spread
    

elo = elo_ratings()
weight = elo.weight_calc(1581, 1544)
change = elo.change_elo(1737, 1577, 'A', 23, 20)
spread = elo.point_spread(1648, 1402)
multiplier = elo.mov_multiplier(1648, 1402, 'A', 23, 20)
print("Weight")
print(weight)
print("Changed")
print(change)
print("Spread")
print(spread)
print("Multiplier")
print(multiplier)


