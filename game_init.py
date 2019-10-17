# Game Init, runs at the start when a game begins
decklist = {}
playerdeck = []
firstvan = None
player1 = None
player2 = None

for i in decklist:
    if decklist[i] == -1:
        firstvan = i
    else:
        playerdeck.append(i * decklist[i])

shuffle(playerdeck)

rightfront = Circle(1,1)
leftfront = Circle(1,3)
centerfront = Circle(1,2,isvanguard = True)
rightback = Circle(2,1)
leftback = Circle(2,3)
centerback = Circle(2,2)
deckzone = Zone('Deck')
dropzone = Zone('Drop')
guardzone = Zone('Guard')
triggerzone = Zone('Trigger')
bindzone = Zone('Bind')
damagezone = Zone('Damage')
handzone = Zone('Hand')
soulzone = Zone('Soul')
gzone = Zone('G')
assistzone = Zone('Assist')

field = [leftfront, centerfront, rightfront,
        leftback, centerback, rightback]


phase = None
turncount = 0
turnplayer = player1
sentinel = False