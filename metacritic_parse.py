#!/usr/bin/env python3
'''
Parses https://www.metacritic.com/game/playstation-4
"Top Playstation 4 Games (By Metascore)" section.

Returns JSON data (title and metacritic score) and
exposes the data via RESTful APIs
'''

import json
import requests
import urllib.parse
import sys
from bs4 import BeautifulSoup
from flask import Flask, Response

# Page to be parsed - code is written specifically for
# metacritic.com/game/<console> pages
metacritic_url = 'https://www.metacritic.com/game/playstation-4'
# Setting User Agent to Chrome... metacritic returns 403
# if user-agent is python (default for requests)
req_user_agent = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}
# Flask Webserver
app = Flask(__name__)


class MetacriticData():
    def __init__(self, url=metacritic_url, header=req_user_agent):
        '''Crawl page and filter data'''
        self.html_content = requests.get(url, headers=header).text
        # The table with the class "clamp-list" currently contains the
        # TOP PLAYSTATION 4 GAMES (By Metascore) data.
        self.souped_content = BeautifulSoup(
            self.html_content, 'html.parser').find(
            'table', {'class': 'clamp-list'})
        # Filter out metascore further, a score div is
        # located inside the 'clamp-score-wrap' div.
        self.metascore_div = self.souped_content.find_all(
            'div', {'class': 'clamp-score-wrap'})

    def generate_data(self):
        '''
        Uses list comprehension to get all game titles (title) and the metacritic score (metascore_raw).
        Then zips the lists into a json blob
        '''
        title = [name.get_text().strip()
                 for name in self.souped_content.find_all('h3')]
        metascore_num = [each.a.div.get_text() for each in self.metascore_div]

        # Create JSON out of the 2 lists (title and metascore_num) ONLY if the
        # lists match in length.
        if len(title) == len(metascore_num):
            self.json_data = json.dumps(
                [{'title': title, 'score': int(score)} for title, score in zip(title, metascore_num)],
                indent=4,
                separators=(',', ': ')
            )
            return self.json_data
        else:
            sys.exit('Data is invalid or metacritic is inaccessible')


@app.route("/", methods=['GET'])
def home_page():
    '''Root page of the site'''
    return """<!doctype html>
            <html>
            <head>
                <title>Hello! This is just a homepage.</title>
            </head>
            <body>
                <p>Hello! This is just a homepage.</p>
                <p>The interesting stuff can be found at :
                    <ul>
                        <li><a href="http://127.0.0.1:5000/games/">http://127.0.0.1:5000/games/</a> : A JSON output containing "Top Playstation 4 Games (By Metascore)" from https://www.metacritic.com/game/playstation-4</li>
                        <br>
                        <li><a href="http://127.0.0.1:5000/games/">http://127.0.0.1:5000/games/(title)</a> : Replace (title) with one on the top 10 to isolate a result</li
                    </ul>
                </p>
            </body>
            </html>"""


@app.route("/games/", methods=['GET'])
def games_all():
    '''Returns "Top Playstation 4 Games (By Metascore)"'''
    return Response(data, mimetype='application/json')


@app.route("/games/<string:title>", methods=['GET'])
def games_filtered(title):
    '''
    Searches through and finds matches in "Top Playstation 4 Games (By Metascore)"
    based on the string added in after /games/
    '''
    unencode_title = urllib.parse.unquote(title)
    j = json.loads(data)
    matching_entries = []
    for dict in j:
        if unencode_title.upper() in dict['title'].upper():
            matching_entries.append(dict)
    if len(matching_entries) == 0:
        return api_return_404()
    else:
        return Response(
            json.dumps(matching_entries, indent=4, separators=(',', ': ')),
            mimetype='application/json'
        )


def api_return_404():
    '''404 JSON blob'''
    return Response(json.dumps({'response': 404,
                                'results': 'No data returned.'},
                               indent=4,
                               separators=(',',
                                           ': ')),
                    mimetype='application/json',
                    status=404)


if __name__ == '__main__':
    data = MetacriticData().generate_data()
    app.run()
