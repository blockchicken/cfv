import random as rm 

def decide_first(you,opp):
    global player1
    global player2
    if rm.randint(0,1) == 0:
        player1 = you
        player2 = opp
        print('You are going First!')
    else:
        player1 = opp
        player2 = you
        print('You are going Second!')

def change_turnplayer():
    global player1
    global player2
    global turnplayer
    if turnplayer == player1:
        turnplayer = player2
    elif turnplayer == player2:
        turnplayer = player1

def get_opponent(player):
    if player == player1:
        return player2
    if player == player2:
        return player1
        
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
    
            
def drive_check(player,num,ezel = False):
    if ezel == False:
        for n in range(num):
            if len(player.deckzone.cardlist) >= num:
                drawn = player.deckzone.cardlist.pop()
                player.triggerzone.add_card(drawn)
                print('Drive Check - {}'.format(drawn.name))
                if drawn.istrigger == True:
                    print('Get! {} Trigger! Power + 10000!'.format(drawn.triggertype))
                    if drawn.triggertype == 'Front':
                        front_trigger(player)
                    else:
                        print('Please Select a Circle with a Unit')
                        fieldlist = list(filter(lambda x: (x.card != None), player.field))
                        powunit = select_from(fieldlist)
                        powunit.card.boostedpower += 10000
                        if drawn.triggertype == 'Critical':
                            critical_trigger(player)
                        elif drawn.triggertype == 'Heal':
                            heal_trigger(player,get_opponent(player))                     
                        elif drawn.triggertype == 'Draw':
                            draw_trigger(player)
                        elif drawn.triggertype == 'Stand':
                            stand_trigger(player)
                trigcard = player.triggerzone.cardlist.pop()
                player.handzone.add_card(trigcard)
            else:
                print('No more cards in deck - Game Over')
                #gameover procedure here
    else:
        pass
        #add in Blazing Lion, Platina Ezel skill effect

def damage_check(player,num):
    for n in range(num):
        if len(player.deckzone.cardlist) >= num:
            drawn = player.deckzone.cardlist.pop()
            player.triggerzone.add_card(drawn)
            print('Drive Check - {}'.format(drawn.name))
            if drawn.istrigger == True:
                print('Get! {} Trigger! Power + 10000!'.format(drawn.triggertype))
                if drawn.triggertype == 'Front':
                    front_trigger(player)
                else:
                    print('Please Select a Circle with a Unit')
                    fieldlist = list(filter(lambda x: (x.card != None), player.field))
                    powunit = select_from(fieldlist)
                    powunit.card.boostedpower += 10000
                    if drawn.triggertype == 'Critical':
                        critical_trigger(player)
                    elif drawn.triggertype == 'Heal':
                        heal_trigger(player,get_opponent(player))                     
                    elif drawn.triggertype == 'Draw':
                        draw_trigger(player)
                    elif drawn.triggertype == 'Stand':
                        stand_trigger(player)
            trigcard = player.triggerzone.cardlist.pop()
            player.damagezone.add_card(trigcard)
        else:
            print('No more cards in deck - Game Over')
    if len(player.deckzone.cardlist) == 0 or len(player.damagezone.cardlist) == 6:
        print('Game Over')
        #Game End Procedure would be kicked off here
        
def discard(card):
    if card in player.handzone.cardlist:
        player.handzone.remove_card(card)
        player.dropzone.add_card(card)
    else:
        print('Error - Card not in Hand...')

def guard_power(zone):
    shieldsum = 0
    for i in zone.cardlist:
        shieldsum += i.currentshield
    return shieldsum

### Triggers ###

def front_trigger(player):
    for circ in player.field:
        if circ.row == 1 and circ.card:
            circ.card.boostedpower += 10000

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

def stand_phase(player):
    # check if skill prevents unit from standing during stand phase
    # skills that activate at start of stand phase
    # stand player's units
    pass
    
def main_phase(player):
    ###option list
    # Call from Hand any cards with grade <= vanguard's
    # Activate Skills, call a "get potential skills that can activate right now" list function
    # Swap Columns (left or Right only)
    # Enter Battle Phase
    pass

def ride_phase(player):
    # generate list of rideable cards, ordered by Grade
    # If list doesn't contain card += Vangaurd's grade and that grade is less than 3:
    # g_assist(player)
    # If list is not empty:
    # Show list to player
    # Player chooses one from list
    # call Ride function
    pass

def battle_phase(player,opponent):
    # Activate any skills on start of battle phase
    ###option list
    # Choose column, including Accel circles
    # Option: If backrow has Boost, give player Boost option
    # Select opponent's column, including access circles
    # Activate any Skills on attack
    ### Note this can be an attack function
    # call Guard step function where the opponent chooses guardians from hand or interceptors and moves them to Guard circle.
    # Calculate opponent's shield based on power + sum of shield on guard
    # Activate any When placed on G skills, including Sentinels
    # Drive Check if applicable
    # Skills upon Drive Check
    # Compare current power of attacker with opponent's target, if power >= target's power, inflict damage = attacker's critical
    # Perform damage checks 
    # skills upon recieving damage
    # skills when unit is sent to dropzone from Guard circle
    # skills when unit is sent to dropzone from field (rear guards only)
    # skills when player's unit's attack hits or "after the battle that this unit attacked/boosted an attack at a vanguard"
    # Return to loop for next attack of units that are not tapped
    # Otherwise, only option left will be Procede to End Phase
    pass

def end_phase(player):
    # gather list of end of turn skills
    # including mandatory skills
    # choose skills from that list
    # once mandatory skills are done allow player to end turn
    # end turn, continuous skills end, boosted power returns to normal, boosted crit/drive/grade etc as well.
    pass

def attack(attacker,target):
    attacker.isrest = True
    print('{} attacks {}.  {} Power vs {} Power.'.format(attacker.name, target.name, attacker.current_power(), target.current_power()))
    if attacker.current_power() >= target.current_power():
        print('Attack hits, proceding to damage step')
        return True
    else:
        return False

def start_turn(player):
    global player1
    global player2
    global turnplayer
    global turncount
    if turncount == 0:
        mulligan(player)
        mulligan(get_opponent(player))
    turncount += 1
    #begin continuous skills for turn
    #start of turn skills

def turn(player):
    start_turn(player)
    stand_phase(player)
    ride_phase(player)
    main_phase(player)
    battle_phase(player,get_opponent(player))
    end_phase(player)

def game(p1,p2):
    global player1
    global player2
    global sentinel
    global turnplayer
    global turncount
    player1, player2 = p1, p2
    decide_first(player1,player2)
    turnplayer = player1
    player1.deck_init()
    player2.deck_init()
    draw(player1,5)
    draw(player2,5)
    while True:
        turn(turnplayer)
        change_turnplayer()
    
        