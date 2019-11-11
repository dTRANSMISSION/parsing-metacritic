app:
	@python metacritic_parse.py

test: 
	@python test.py -v

bootstrap:
	@pip install -r requirements.txt