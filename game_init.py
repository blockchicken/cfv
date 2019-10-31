import pandas as pd


### Import the card list
cardlist = pd.read_csv('cardlist.csv',index_col=0)
carddb = {}
for x in cardlist.itertuples():
    carddb[x.Index] = Card(*x)

### Import the decklists

p1dek = {5: -1, 6: 4, 7: 4, 8: 4, 9: 4, 10: 4, 11: 4, 12: 4, 13: 2, 14: 4, 15: 4, 16: 3, 17: 4, 18: 4} #Royal Paladin Trial Deck
p2dek = {19: -1, 20: 4, 21: 4, 22: 4, 23: 4, 24: 4, 25: 4, 26: 4, 27: 2, 28: 4, 29: 4, 30: 3, 31: 4, 32: 4} #Kagero Trial Deck
#note for testing purposes, these two Trial Decks are included automatically

### Global vars
playernames = set()
player1 = None
player2 = None
turnplayer = player1
winner = None
loser = None
sentinel = None
turncount = 0
turnattackcount = 0
ezel = 0