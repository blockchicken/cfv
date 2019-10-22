import random as rm 

def decide_first(you,opp):
    if rm.randint(0,1) == 0:
        player1 = you
        player2 = opp
        print('You are going First!')
    else:
        player1 = opp
        player2 = you
        print('You are going Second!')

def change_turnplayer():
    if turnplayer == player1:
        turnplayer = player2
    elif turnplayer == player2:
        turnplayer = player1
        
def shuffle(deck):
    rm.shuffle(deck)

def select_from(z):
    #Takes list, allows player to select from list of cards, circles, etc
    print('Select from the following:')
    for i in range(len(z)):
        print(str(i) + ' : ' + z[i].name)
    while True:
        selection = int(input())
        if selection >= 0 and selection <= len(z):
            return z[selection]
        else:
            print('Error - not in list')
    
def draw(player, num):
    for n in range(num):
        if len(player.deckzone.cardlist) >= num:
            drawn = player.deckzone.cardlist.pop()
            player.handzone.add_card(drawn)
        else:
            print('No more cards in deck - Game Over')
            # gameover procedure here

def mulligan(player):
    print('Your hand is currently:')
    print([i.name for i in player.handzone.cardlist])
    print('How many cards would you like to mulligan?')
    numback = 0
    while numback <= 5 and numback >= 0:
        numback = int(input())
        for n in range(numback):
            print('Please choose a card:')
            chosen = select_from(player.handzone.cardlist)
            player.handzone.remove_card(chosen)
            player.deckzone.add_card(chosen,bottom=True)
        draw(player, numback)
        shuffle(player.deckzone.cardlist)
        numback = -1
    
            
def drive_check(num,ezel = False):
    if ezel == False:
        for n in range(num):
            if len(deckzone.cardlist) >= num:
                drawn = deckzone.cardlist.pop()
                triggerzone.add_card(drawn)
                print('Drive Check - {}'.format(drawn.name))
                if drawn.istrigger == True:
                    print('Get! {} Trigger! Power + 10000!'.format(drawn.triggertype))
                    if drawn.triggertype == 'front':
                        front_trigger()
                    else:
                        print('Please Select a Circle with a Unit')
                        fieldlist = list(filter(lambda x: (x.card != None), field))
                        powunit = select_from(fieldlist)
                        powunit.card.currentpower += 10000
                        if drawn.triggertype == 'critical':
                            critical_trigger()
                        elif drawn.triggertype == 'heal':
                            heal_trigger()                     
                        elif drawn.triggertype == 'draw':
                            draw_trigger()
                        elif drawn.triggertype == 'stand':
                            stand_trigger()
                trigcard = triggerzone.cardlist.pop()
                handzone.add_card(trigcard)
            else:
                print('No more cards in deck - Game Over')
                #gameover procedure here
    else:
        pass
        #add in Blazing Lion, Platina Ezel skill effect

def damage_check(num):
    for n in range(num):
        if len(deckzone.cardlist) >= num:
            drawn = deckzone.cardlist.pop()
            triggerzone.add_card(drawn)
            print('Drive Check - {}'.format(drawn.name))
            if drawn.istrigger == True:
                print('Get! {} Trigger! Power + 10000!'.format(drawn.triggertype))
                pass 
                #here would go the complex Trigger Logic
            trigcard = triggerzone.cardlist.pop()
            damagezone.add_card(trigcard)
        else:
            print('No more cards in deck - Game Over')
    if len(deckzone.cardlist) == 0 or len(damagezone.cardlist) == 6:
        print('Game Over')
        #Game End Procedure would be kicked off here
        
def discard(card):
    if card in handzone.cardlist:
        handzone.remove_card(card)
        dropzone.add_card(card)
    else:
        print('Error - Card not in Hand...')

def to_guard(origin,card):
    guardzone.add_card(card)
    origin.remove_card(card)

def guard_power(zone):
    shieldsum = 0
    for i in zone.cardlist:
        shieldsum += i.currentshield
    return shieldsum

### Triggers ###

def front_trigger(player):
    for circ in player.field:
        if circ.row == 1 and circ.card:
            circ.card.currentpower += 10000

def draw_trigger(player):
    draw(player,1)

def critical_trigger(player):
    critfield = list(filter(lambda x: (x.card != None), player.field))
    critunit = select_from(critfield)
    critunit.card.currentcritical += 1

def heal_trigger(player,opponent):
    if len(player.damagezone.cardlist) >= len(opponent.damagezone.cardlist):
        #select card in damagezone
        healcard = select_from(player.damagezone.cardlist)
        player.damagezone.remove_card(healcard)
        player.dropzone.add_card(healcard)
    else:
        pass

def stand_trigger(player):
    standfield = list(filter(lambda x: (x.card != None), player.field))
    standunit = select_from(standfield.remove('centerfront'))
    standunit.card.isrest = False
            
### end of Triggers ###

def sentinel():
    sentinel = True

def end_of_battle(player):
    sentinel = False
    if len(player.guardzone.cardlist) > 0:
        for i in player.guardzone.cardlist:
            player.guardzone.remove_card(i)
            player.dropzone.add_card(i)

def add_equip_guage(player,card,num):
    for n in range(num):
        if len(player.deckzone.cardlist) >= num:
            topcard = player.deckzone.cardlist.pop()
            card.equipgauge.append(topcard)
        else:
            print('No more cards in deck - Game Over')

def soul_charge(player,num):
    for n in range(num):
        if len(player.deckzone.cardlist) >= num:
            charged = player.deckzone.cardlist.pop()
            player.soulzone.add_card(charged)
        else:
            print('No more cards in deck - Game Over')

def soul_blast(player,num):
    for n in range(num):
        print('Soulblast:')
        soulcard = select_from(soulzone)
        soulzone.remove_card(soulcard)
        dropzone.add_card(soulcard)

def g_assist(player):
    currentgrade = player.centerfront.card.grade
    checked = player.deckzone.cardlist[:5]
    selection = []
    for i in checked:
        if i.grade == currentgrade + 1:
            selection.append(i)
    if selection == []:
        return('No cards in top 5')
    selected = select_from(selection)
    player.handzone.add_card(selected)
    player.deckzone.remove_card(selected)
    shuffle(player.deckzone.cardlist)
    print('Select two cards to remove from the game:')
    print('First selection:')
    firstassist = select_from(player.handzone.cardlist)
    player.assistzone.add_card(firstassist)
    player.handzone.remove_card(firstassist)
    print('Second selection:')
    secondassist = select_from(player.handzone.cardlist)
    player.assistzone.add_card(secondassist)
    player.handzone.remove_card(secondassist)