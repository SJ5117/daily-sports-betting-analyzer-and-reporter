This app is intended to be used with [The Odds API](https://the-odds-api.com/). 

This app takes CSV inputs in the format of this below for matchup bets:
market,line,side,odds,conf_lev
"h2h","Brooklyn Nets vs Boston Celtics, Boston Celtics",Boston Celtics,-128,High
"spreads","Brooklyn Nets vs Boston Celtics, Boston Celtics -9",Boston Celtics,-194,Medium
"totals","Brooklyn Nets vs Boston Celtics, Under 227.5",Under,-189,High
"h2h","Orlando Magic vs Oklahoma City Thunder, Oklahoma City Thunder",Oklahoma City Thunder,-165,High
"spreads","Orlando Magic vs Oklahoma City Thunder, Oklahoma City Thunder -2.5",Oklahoma City Thunder,-188,Medium
"totals","Orlando Magic vs Oklahoma City Thunder, Under 223",Under,-191,High

...and this for player prop bets:
line,side,odds,conf_lev
"Jrue Holiday, Over 12.5",1,+181,Medium High
"Dorian Finney-Smith, Under 7.5 ",2,-177,Medium
"Jaylen Brown, Under 22.5",2,+182,Medium High
"Derrick White, Under 14.5",2,+183,Medium
"Kristaps Porzingis, Over 19.5",1,+188,High
"Mikal Bridges, Under 22.5",2,+183,Medium
"Nic Claxton, Under 12.5",2,+182,Medium High

conf_lev is retrieved from a custom GPT.

When running either NBAAPI_matchup.py or NBAAPI_player.py, make sure that you change the date at the top and add a directory named ./archive so that the script can clean up your directory. Either Python script will analyze the CSV file given in the format: playerOutput_2_13_24.csv or matchupOutput_2_13_24.csv be sure to change the date to today if that's the route yu want to go.

Good luck!
