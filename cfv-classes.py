# The core class, everything in the card game revolves around cards
class Card:
    def __init__(self, cardid, name, clan, nation, grade, power, shield, critical = 1,
    skills = None, marker = None, istrigger = False,
    triggertype = None, boost = False, intercept = False, drive = 1, flavor = None,
    image = None, tags = None):
        self.cardid = cardid
        self.name = name
        self.clan = clan
        self.nation = nation
        self.grade = grade
        self.power = power
        self.shield = shield
        self.critical = critical
        if skills is None:
            skills = []
        self.skills = skills
        self.marker = marker
        self.istrigger = istrigger
        self.triggertype = triggertype
        self.boost = boost
        self.intercept = intercept
        self.drive = drive
        self.flavor = flavor
        self.image = image
        if skills is None:
            tags = []
        self.tags = tags
    
    def get_name(self):
        return self.name
    
    def get_id(self):
        return self.cardid
    
### Example Little_Sage_Marron = Card(1,"Little Sage Marron","Royal Paladin","United Sanctuary",1,8000,10000, boost = True)

# Define Game Cards, Cards that will be used in the game

class Gamecard(Card):
    def __init__(self
                 , *args):
        self.__dict__ = args[0].__dict__.copy()
        self.faceup = True
        self.boostedpower = 0
        self.currentcritical = self.critical
        self.currentdrive = self.drive
        self.equipgauge = []
        self.isrest = False
        self.currentshield = self.shield
        self.canintercept = self.intercept
        self.canboost = self.boost
        self.names = [self.name]
        self.gainedskills = []
    
    def counter_blast(self):
        if self.faceup == True:
            self.faceup = False
        else:
            print('Error - Already Facedown')
    
    def counter_charge(self):
        if self.faceup == False:
            self.faceup = True
        else:
            print('Error - Already Faceup')

    def current_power(self):
        return self.boostedpower + self.power
       

# Define Circles


class Circle:
    def __init__(self, name, row, column, card = None, isaccel = False, marker = None, isvanguard = False, owner = None):
        self.name = name
        self.row = row
        self.column = column
        self.isaccel = isaccel
        self.marker = []
        self.card = card
        self.isvanguard = isvanguard
        self.owner = owner

    def add_marker(self,mark):
        self.marker.append(mark)

    def retire(self):
        if self.card != None:
            dropzone.add_card(self.card)
            if len(self.card.equipgauge) > 0:
                for i in equipgauge:
                    dropzone.add_card(i)
        self.card = None
    def call_card(self,card):
        self.retire()
        self.card = card
    
    def get_card_power(self):
        if self.card:
            markerpow = 0
            if self.marker:
                for i in self.marker:
                    if i == 'Force 1' and self.owner == turnplayer.name:
                        markerpow += 10000
                    if i == 'Accel 1' and self.owner == turnplayer.name:
                        markerpow += 10000
                    if i == 'Accel 2' and self.owner == turnplayer.name:
                        markerpow += 5000
                    if i == 'Protect 2':
                        markerpow += 5000
            return self.card.current_power() + markerpow
                        
    def get_card_shield(self):
        if self.card:
            markershield = 0
            if self.marker:
                for i in self.marker:
                    if i == 'Protect 2':
                        markershield += 10000
            return self.card.currentshield + markershield
    
    def get_card_critical(self):
        if self.card:
            if 'Force 2' in self.marker:
                return self.card.currentcritical + 1
            else:
                return self.card.currentcritical
    
# Define Zones


class Zone:
    def __init__(self, name, cardlist = None):
        self.name = name
        if cardlist is None:
            cardlist = []
        self.cardlist = cardlist

    def add_card(self,card,bottom=False):
        if not bottom:
            self.cardlist.append(card)
        else:
            self.cardlist.insert(0,card)
        
    def remove_card(self,card):
        self.cardlist.remove(card)
    
    def empty_list(self):
        self.cardlist = []
        


# Define Players


class Player:
    def __init__(self, name, decklist, field = [],isactive = False, firstvan = None, clan = None, nation = None
                , chosenaccel = None, chosenforce = None, chosenprotect = None):
        global playernames
        if name in playernames:
            raise ValueError('Player name already exists...')
        else:
            playernames.add(name)
        self.name = name
        self.decklist = decklist
        self.clan = clan
        self.nation = nation
        self.field = field
        self.isactive = isactive
        self.firstvan = firstvan
        self.rightfront = Circle('rightfront',1,1,owner=name)
        self.leftfront = Circle('leftfront',1,3,owner=name)
        self.centerfront = Circle('centerfront',1,2,isvanguard = True,owner=name)
        self.rightback = Circle('rightback',2,1,owner=name)
        self.leftback = Circle('leftback',2,3,owner=name)
        self.centerback = Circle('centerback',2,2,owner=name)
        self.field = [self.leftfront, self.centerfront, self.rightfront,
                      self.leftback, self.centerback, self.rightback]
        self.deckzone = Zone('Deck')
        self.dropzone = Zone('Drop')
        self.guardzone = Zone('Guard')
        self.triggerzone = Zone('Trigger')
        self.bindzone = Zone('Bind')
        self.damagezone = Zone('Damage')
        self.handzone = Zone('Hand')
        self.soulzone = Zone('Soul')
        self.gzone = Zone('G')
        self.assistzone = Zone('Assist')
        self.chosenaccel = None
        self.chosenforce = None
        self.chosenprotect = None
        self.brandt = 0
        
        
    def deck_init(self):
        self.deckzone.cardlist = []
        for i in self.decklist:
            if self.decklist[i] == -1:
                self.firstvan = Gamecard(carddb[i])
            else:
                for n in range(self.decklist[i]):
                    self.deckzone.cardlist.append(Gamecard(carddb[i]))
        shuffle(self.deckzone.cardlist)
        
        # ex. p1dek = {5: -1, 6: 4, 7: 4, 8: 4, 9: 4, 10: 4, 11: 4, 12: 4, 13: 2, 14: 4, 15: 4, 16: 3, 17: 4, 18: 4}
    
    def set_firstvan(self):
        self.centerfront.call_card(self.firstvan)
        
    def ride_card(self,ride):
        # attempt When this card is ridden upon skills
        self.soulzone.add_card(self.centerfront.card)
        self.centerfront.card = ride
        if self.centerfront.card.marker:
            choose_markertype(self,self.centerfront.card.marker)
            place_marker(self,self.centerfront.card.marker)
        # attempt When Placed on VC skills
        
        
        
class Skill:
    def __init__(self, skillid, name, kind, effect, requirement, area, timing = []):
        self.skillid = skillid
        self.name = name
        self.kind = kind
        self.effect = effect
        self.requirement = requirement #ex. If cost is Soul Blast 2, check soul has >= 2 cards.
        self.area = area
        self.timing = timing
        
    def get_timings(self):
        return self.timing
    
    def use_skill(self):
        return skillid #here i'd want it to call the effect of that skill... somehow
    
    def is_continuous(self):
        return self.kind == 'Cont'