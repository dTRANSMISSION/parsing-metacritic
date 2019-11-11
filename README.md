Parsing Metacritic
==============================

What Is This?
-------------
This is a simple Python/Flask application that parses the "Top Playstation 4 Games (By Metascore)" section on https://www.metacritic.com/game/playstation-4.

Returns the title and score as JSON and exposes the data via RESTful APIs.

This application is designed to run on python3.

How To Use This
---------------

1. Install the dependencies with `make bootstrap` 
    * If you need to install directly with pip, run `pip install -r requirements.txt` (pip can also be pip3)
2. Startup the app with `make app`
    * You can also startup directly via running `python metacritic_parse.py`
3. Navigate to http://localhost:5000 in a web broswer

Testing
-------

1. Install the dependencies with `make bootstrap` 
    * If you need to install directly with pip, run `pip install -r requirements.txt` (pip can also be pip3)
2. Run `make test`
    * This invokes `python test.py -v`