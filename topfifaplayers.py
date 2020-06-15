from requests import get
from bs4 import BeautifulSoup
import pandas as pd

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
}

url = 'https://www.ea.com/games/fifa/fifa-20/ratings/fifa-20-player-ratings-top-100'

response = get(url, headers=header)
html_soup = BeautifulSoup(response.text, 'html.parser')
player_container = html_soup.find_all(
    'ea-container', attrs={'slot': 'container'})

names = []
ranks = []
teams = []
ratings = []

for player in player_container:

    player_data = player.find_all(["h3", "div", "p"])
    counter = 0
    for tag_elems in player_data:
        for string in tag_elems:

            if counter == 0:
                names.append(string)

            if counter == 1:
                ranks.append(string)

            if counter == 2:
                teams.append(string)

            if counter == 3:
                ratings.append(string)
        counter += 1


fifa_ratings = pd.DataFrame({'name': names,
                             'rank': ranks,
                             'rating': ratings,
                             'team': teams
                             })

fifa_ratings['rank'] = pd.to_numeric(fifa_ratings['rank'])
fifa_ratings = fifa_ratings.sort_values('rank')

print(fifa_ratings.head(5))
fifa_ratings.to_csv('fifa.csv', index=False)
