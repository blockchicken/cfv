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

def select_from_list(z):
    #Takes list, allows player to select from list of cards, circles, etc
    print('Select from the following:')
    for i in range(len(z)):
        print(str(i) + ' : ' + z[i])
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
            print('Damage Check - {}'.format(drawn.name))
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
        
def discard(player,card):
    if card in player.handzone.cardlist:
        player.handzone.remove_card(card)
        player.dropzone.add_card(card)
    else:
        print('Error - Card not in Hand...')

def guard_power(player):
    shieldsum = 0
    for i in player.guardzone.cardlist:
        shieldsum += i.currentshield
    return shieldsum

### Triggers ###

def front_trigger(player):
    for circ in player.field:
        if circ.row == 1 and circ.card:
            circ.card.boostedpower += 10000

def draw_trigger(player):
    if player.brandt > 1 and player.handzone.cardlist != []:
        player(discard)
    else:
        draw(player,1)

def critical_trigger(player):
    if player.brandt > 0:
        player.centerfront.card.currentcritical -= 1
    else:
        print('Please select a unit to receive the Critical!')
        critfield = list(filter(lambda x: (x.card != None), player.field))
        critunit = select_from(critfield)
        critunit.card.currentcritical += 1

def heal_trigger(player,opponent):
    if player.brandt > 0:
        damage_check(player)
    elif len(player.damagezone.cardlist) >= len(opponent.damagezone.cardlist):
        #select card in damagezone
        print('Please select a unit from your Damage Zone to Heal!')
        healcard = select_from(player.damagezone.cardlist)
        player.damagezone.remove_card(healcard)
        player.dropzone.add_card(healcard)
    else:
        return

def stand_trigger(player):
    print('Please select a rear-guard to stand.')
    standfield = list(filter(lambda x: (x.card != None), player.field))
    standunit = select_from(standfield.remove('centerfront'))
    standunit.card.isrest = False
            
### end of Triggers ###

def choose_markertype(player,marker):
    if marker == 'Force':
        if player.chosenforce:
            return
        markerchoice = select_from_list(['Force I','Force II'])
        if markerchoice == 'Force I':
            player.chosenforce = 1
        if markerchoice == 'Force II':
            player.chosenforce = 2
    if marker == 'Accel':
        if player.chosenaccel:
            return
        markerchoice = select_from_list(['Accel I','Accel II'])
        if markerchoice == 'Accel I':
            player.chosenaccel = 1
        if markerchoice == 'Accel II':
            player.chosenaccel = 2
    if marker == 'Protect':
        if player.chosenprotect:
            return
        markerchoice = select_from_list(['Protect I','Protect II'])
        if markerchoice == 'Protect I':
            player.chosenprotect = 1
        if markerchoice == 'Protect II':
            player.chosenprotect = 2

def place_marker(player,markertype):
    if markertype == 'Force':
        #player selects circle
        circlist = []
        for i in player.field:
            circlist.append(i)
        chosencirc = select_from(circlist)
        #gain player's force type
        chosencirc.add_marker('Force {}'.format(player.chosenforce))
        
    elif markertype == 'Accel':
        maxcol = 3
        mincol = 1
        colcount = 0
        for i in list(filter(lambda x: (x.row == 1), player.field)):
            colcount += 1
            if i.col > maxcol:
                maxcol = i.col
            if i.col < mincol:
                mincol = i.col
        if colcount % 2 == 0:
            maxcol += 1
            player.field.append(Circle(name='Accel Circle {}'.format(maxcol),row=1,column=maxcol,owner=player.name,isaccel=True,marker = 'Accel {}'.format(player.chosenaccel)))
        else:
            mincol -= 1
            player.field.append(Circle(name='Accel Circle {}'.format(mincol),row=1,column=mincol,owner=player.name,isaccel=True,marker = 'Accel {}'.format(player.chosenaccel)))
        
    elif markertype == 'Protect':
        #player gains Protect card if ProtectI
        if player.chosenprotect == 1:
            player.handzone.add_card(carddb[1]) #carddb[1] = Protect I card
        if player.chosenprotect == 2:
            circlist = []
            for i in list(filter(lambda x: (x.card.isvanguard == False), player.field)):
                circlist.append(i)
            chosencirc = select_from(circlist)
            #gain player's protect type
            chosencirc.add_marker('Protect 2')


def sentinel():
    global sentinel
    sentinel = True

def end_of_battle(player,opponent):
    global sentinel
    sentinel = False
    if len(opponent.guardzone.cardlist) > 0:
        for i in opponent.guardzone.cardlist:
            opponent.guardzone.remove_card(i)
            opponent.dropzone.add_card(i)
    #activate player's End of battle skills
    #activate opponent's End of battle skills

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

def choose_guardians(player,restriction=None,nosentinel=False):
    guardlist = []
    for i in player.handzone.cardlist:
        if nosentinel and 'Sentinel' in i.tags:
            continue
        elif restriction:
            if i.grade in restriction:
                continue
        else:
            guardlist.append(i)
    while True:
        print('Choose a guardian from your hand?')
        print([x.name for x in guardlist])
        guardyesno = select_from_list(['Yes','No'])
        if guardyesno == 'Yes':
            guardcard = select_from(guardlist)
            player.guardzone.add_card(guardcard)
            player.handzone.remove_card(guardcard)
        else:
            return
    guardlist = []
    for j in list(filter(lambda x: (x.card != None), player.field)):
        if j.card.canintercept:
            guardlist.append(j)
    if guardlist != []:
        while True:
            print('Intercept?')
            print([x.card.name for x in guardlist])
            guardyesno = select_from_list(['Yes','No'])
            if guardyesno == 'Yes':
                guardcard = select_from([x.card.name for x in guardlist])
                player.guardzone.add_card(guardcard.card)
                player.guardcard.card=None
            else:
                return
    
def stand_phase(player):
    # check if skill prevents unit from standing during stand phase
    # skills that activate at start of stand phase
    # stand player's units
    unitfield = list(filter(lambda x: (x.card != None), player.field))
    for c in unitfield:
        c.card.isrest=False
    
def main_phase(player):
    ###option list
    # Call from Hand any cards with grade <= vanguard's
    # Activate Skills, call a "get potential skills that can activate right now" list function
    # Swap Columns (left or Right only)
    # Enter Battle Phase
    print('Main Phase. Please select from the following options:')
    while True:
        optionlist = ['Call from Hand','Activate Skill','Swap Columns','To Battle Phase']
        selection = select_from_list(optionlist)
        if selection == 'Call from Hand':
            print(player.centerfront.card.grade)
            print(player.handzone.cardlist[0].grade)
            calllist = []
            for i in player.handzone.cardlist:
                if i.grade <= player.centerfront.card.grade:
                    calllist.append(i)
            callselect = select_from(calllist)
            print('Which circle do you want to call to?')
            select_from(list(filter(lambda x: (x.name != 'centerfront'), player.field))).call_card(callselect)
        elif selection == 'Activate Skill':
            pass
        elif selection == 'Swap Columns':
            colselect = select_from_list(['Right','Left'])
            if colselect == 'Right':
                player.rightfront.card, player.rightback.card = player.rightback.card, player.rightfront.card
        else:
            return
    

def ride_phase(player):
    # generate list of rideable cards, ordered by Grade
    ridelist = []
    for i in player.handzone.cardlist:
        if i.grade == player.centerfront.card.grade + 1 or i.grade == player.centerfront.card.grade:
            ridelist.append(i)
    # If list doesn't contain card += Vangaurd's grade and that grade is less than 3:
    if ridelist == []:
        g_assist(player)
    # Now post-assist, check for rideability
    if ridelist != []:
        sorted(ridelist, key=lambda x: x.grade, reverse=True)
        print('Do you wish to ride one of these cards?')
        print([x.name for x in ridelist])
        rideyesno = select_from_list(['Yes','No'])
        if rideyesno == 'Yes':
            ridecard = select_from(ridelist)
            player.ride_card(ridecard)
            player.handzone.remove_card(ridecard)

def battle_phase(player,opponent):
    # Activate any skills on start of battle phase
    ###option list
    while True:
        optionlist = ['Attack','To End Phase']
        selection = select_from_list(optionlist)
        if selection == 'Attack':
            collist = []
            for i in player.field:
                if i.row == 1 and i.card and i.card.isrest == False:
                    print(i.name, i.card.name)
                    collist.append(i)
            if collist == []:
                return
            # Choose column, including Accel circles
            chosencol = select_from(collist)
            behind = list(filter(lambda x: (x.column == chosencol.column and x.row == 2), player.field))[0]
            if behind.card:
                if behind.card.boost and behind.card.isrest == False:
                    print('Boost with {}?'.format(behind.card.name))
                    if select_from_list(['Yes','No']) == 'Yes':
                        behind.card.isrest = True
                        chosencol.card.boostedpower += behind.card.current_power()
            # Select opponent's column, including accel circles
            oppcollist = []
            for i in opponent.field:
                if i.row == 1 and i.card:
                    print(i.name, i.card.name)
                    oppcollist.append(i)
            targetcol = select_from(oppcollist)
            # Activate any Skills on attack
            ### Attack!!!
            choose_guardians(opponent)
            # Calculate opponent's shield based on power + sum of shield on guard
            targetcol.card.boostedpower += guard_power(opponent)
            # Activate any When placed on G skills, including Sentinels
            # Drive Check if applicable
            if chosencol.isvanguard == True:
                drive_check(player,chosencol.card.currentdrive,ezel)
            # Skills upon Drive Check
            if attack(chosencol.card,targetcol.card):
                if targetcol.isvanguard == True:
                    #damage check
                    damage_check(opponent,chosencol.card.currentcritical)
                else:
                    print('{} is retired'.format(targetcol.card.name))
                    targetcol.retire()
            if targetcol.card:
                targetcol.card.boostedpower -= guard_power(opponent)
            end_of_battle(player,opponent)
            # skills when unit is sent to dropzone from Guard circle
            # skills when unit is sent to dropzone from field (rear guards only)
            # skills when player's unit's attack hits or "after the battle that this unit attacked/boosted an attack at a vanguard"
        else:
            return


def end_phase(player):
    global turnattackcount
    # gather list of end of turn skills
    # including mandatory skills
    # choose skills from that list
    # once mandatory skills are done allow player to end turn
    # end turn, continuous skills end, boosted power returns to normal, boosted crit/drive/grade etc as well.
    for i in player.field:
        if i.card:
            i.card.boostedpower = 0
            i.card.currentdrive = i.card.drive
            i.card.currentcritical = i.card.critical
            i.card.currentshield = i.card.shield
            i.card.faceup = True
            i.card.names = [i.card.name]
            i.card.gainedskills = []
    player.brandt = 0
    opp = get_opponent(player)
    for i in opp.field:
        if i.card:
            i.card.boostedpower = 0
            i.card.currentdrive = i.card.drive
            i.card.currentcritical = i.card.critical
            i.card.currentshield = i.card.shield
            i.card.names = [i.card.name]
            i.card.gainedskills = []
    turnattackcount = 0
            
def attack(attacker,target):
    global turnattackcount
    turnattackcount += 1
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
    player1.centerfront.call_card(player1.firstvan)
    player2.centerfront.call_card(player2.firstvan)
    draw(player1,5)
    draw(player2,5)
    while not winner:
        turn(turnplayer)
        change_turnplayer()
    return('Game Over - Winner: {}, Loser: {}'.format(winner,loser))
    # here is where it would output the game result
    
        