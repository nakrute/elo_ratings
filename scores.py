import requests
from bs4 import BeautifulSoup

city_team = {"Vegas": "Raiders",
             "Jets" : "Jets",
             "Indianapolis" : "Colts",
             "Houston" : "Texans",
             "Cleveland" : "Browns",
             "Tennessee" : "Titans",
             "Detroit" : "Lions",
             "Chicago" : "Bears",
             "Jacksonville" : "Jaguars",
             "Orleans" : "Saints",
             "Atlanta" : "Falcons",
             "Angeles" : "Rams",
             "Arizona" : "Cardinals",
             "Giants" : "Giants",
             "Seattle" : "Seahawks",
             "England" : "Patriots",
             "Philadelphia" : "Eagles",
             "Bay" : "Packers",
             "Denver" : "Broncos",
             "City" : "Chiefs",
             "Washington" : "Washington",
             "Pittsburgh" : "Steelers",
             "Buffalo" : "Bills",
             "Francisco" : "49ers",
             "Baltimore" : "Ravens",
             "Dallas" : "Cowboys",
             "Carolina" : "Panthers",
             "Tampa" : "Buccaneers",
             "Cincinatti" : "Bengals",
             "Miami" : "Dolphins"}

class Scores(object):
    weeks = list(range(1, 13))
    #url_base = "https://www.espn.com/nfl/scoreboard/_/year/2020/seasontype/2/week/"
    url_base= "http://www.espn.com/nfl/bottomline/scores"
    def get_url(self):
        url_week = str(Scores.url_base)
        return url_week

    def request_data(self, url_full):
        res = requests.get(url_full)
        res.raise_for_status()
        return res

    def soup_and_create_list(self, html):
        soup = BeautifulSoup(html.content, "html.parser")
        score_list = str(soup).split('?')
        return score_list

    def parse_list(self, item, delimit):
        parsed = item.split(str(delimit))
        return parsed

    def key_change(self, dict, key):
        pass

    def write_data(self, data_dict):
        pass

score_uploader = Scores()

url = score_uploader.get_url()
data = score_uploader.request_data(url)
score_list = score_uploader.soup_and_create_list(data)
for score in score_list:
    p = score_uploader.parse_list(score, "20")
    print(p)
    try:
        first_names = ["Las", "New", "NY", "Kansas", "Green", "San"]
        team_one = p[1].strip("%").split("=")[1].strip("^")
        team_two = p[5].strip("%").strip("^")
        if team_one in first_names:
            team_one = p[2].strip("%")
            score_one = p[3].strip("%")
        if team_one not in first_names:
            team_one = team_one
            score_one = p[2].strip("%")
        if team_two in first_names:
            team_two = p[6].strip("%").strip("^")
            score_two = p[7].strip("%")
        if team_two not in first_names:
            team_two = team_two
            score_two = p[6].strip("%")
        if score_one == "":
            score_one = 0
        if score_two == "":
            score_two = 0
        print({team_one : score_one, team_two : score_two})
    except Exception:
        print("FAILED")

