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

def shuffle(deck):
    rm.shuffle(deck)

def select_from(player, cardlist):
    print('Select from the following:')
    for i in range(len(cardlist)):
        print(str(i) + ' : ' + cardlist[i].name)
    while True:
        selection = int(input())
        if selection >= 0 and selection <= len(cardlist):
            return cardlist[selection]
        else:
            print('Error - not in list')

def select_circle(player, f):
    print('Select from the following:')
    for i in range(len(player.f)):
        print(str(i) + ' : ' + str(player.f))
    while True:
        selection = int(input())
        if selection >= 0 and selection <= len(player.f):
            return player.f[selection]
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
    print([i.name for i in player.deckzone.cardlist])
    print('How many cards would you like to mulligan?')
    choice = int(input())
    for c in range(choice):
        
            
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
                        powunit = select_circle(fieldlist)
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

def front_trigger():
    for circ in field:
        if circ.row == 1 and circ.card:
            circ.card.currentpower += 10000

def draw_trigger():
    draw(1)

def critical_trigger():
    critfield = list(filter(lambda x: (x.card != None), field))
    critunit = select_circle(critfield)
    critunit.card.currentcritical += 1

def heal_trigger():
    #if len(damagezone) >= opponent's:
    #select card in damagezone
    #damagezone.remove_card(selected card)
    pass

def stand_trigger():
    standfield = list(filter(lambda x: (x.card != None), field))
    standunit = select_circle(standfield.remove('centerfront'))
    standunit.card.isrest = False
            
### end of Triggers ###

def sentinel():
    sentinel = True

def end_of_battle():
    sentinel = False
    if len(guardzone.cardlist) > 0:
        for i in guardzone.cardlist:
            guardzone.remove_card(i)
            dropzone.add_card(i)

def add_equip_guage(circle,num):
    for n in range(num):
        if len(deckzone.cardlist) >= num:
            topcard = deckzone.cardlist.pop()
            circle.card.equipgauge.append(topcard)
        else:
            print('No more cards in deck - Game Over')

def soul_charge(num):
    for n in range(num):
        if len(deckzone.cardlist) >= num:
            charged = deckzone.cardlist.pop()
            soulzone.add_card(charged)
        else:
            print('No more cards in deck - Game Over')

def soul_blast(num):
    for n in range(num):
        print('Soulblast:')
        soulcard = select_from(soulzone)
        soulzone.remove_card(soulcard)
        dropzone.add_card(soulcard)

def g_assist():
    currentgrade = centerfront.grade
    checked = deckzone.cardlist[:5]
    selection = []
    for i in checked:
        if checked.grade == currentgrade + 1:
            selection.append(i)
    if selection == []:
        return('No cards in top 5')
    selected = select_from(selection)
    handzone.add_card(selected)
    deckzone.remove_card(selected)
    shuffle(deckzone)
    print('Select two cards to remove from the game:')
    print('First selection:')
    firstassist = select_from(handzone.cardlist)
    assistzone.add_card(firstassist)
    handzone.remove_card(firstassist)
    print('Second selection:')
    secondassist = select_from(handzone.cardlist)
    assistzone.add_card(secondassist)
    handzone.remove_card(secondassist)