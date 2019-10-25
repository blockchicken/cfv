# The core class, everything in the card game revolves around cards
class Card:
    def __init__(self, cardid, name, clan, nation, grade, power, shield, critical = 1,
    skill1 = None, skill2 = None, skill3 = None, marker = None, istrigger = False,
    triggertype = None, boost = False, intercept = False, drive = 1, flavor = None,
    image = None, tags = []):
        self.cardid = cardid
        self.name = name
        self.clan = clan
        self.nation = nation
        self.grade = grade
        self.power = power
        self.shield = shield
        self.critical = critical
        self.skill1 = skill1
        self.skill2 = skill2
        self.skill3 = skill3
        self.marker = marker
        self.istrigger = istrigger
        self.triggertype = triggertype
        self.boost = boost
        self.intercept = intercept
        self.drive = drive
        self.flavor = flavor
        self.image = image
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
    def __init__(self, name, row, column, card = None, isaccel = False, marker = None, markercount = 0, isvanguard = False):
        self.name = name
        self.row = row
        self.column = column
        self.isaccel = isaccel
        self.marker = marker
        self.card = card
        self.markercount = markercount
        self.isvanguard = isvanguard

    def add_marker(self,marker):
        self.marker = marker
        self.markercount += 1
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
        


# Define Zones


class Zone:
    def __init__(self, name, cardlist = []):
        self.name = name
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
    def __init__(self, name, decklist, handzone=None, deckzone=None
                 ,dropzone=None, guardzone=None, triggerzone=None, bindzone=None, damagezone=None, soulzone=None, gzone=None
                 ,assistzone=None,field = [],isactive = False, firstvan = None, clan = None, nation = None):
        self.name = name
        self.decklist = decklist
        self.clan = clan
        self.nation = nation
        self.field = field
        self.handzone = handzone
        self.deckzone = deckzone
        self.dropzone = dropzone
        self.guardzone = guardzone
        self.triggerzone = triggerzone
        self.bindzone = bindzone
        self.damagezone = damagezone
        self.soulzone = soulzone
        self.gzone = gzone
        self.assistzone = assistzone
        self.isactive = isactive
        self.firstvan = firstvan
        self.rightfront = Circle('rightfront',1,1)
        self.leftfront = Circle('leftfront',1,3)
        self.centerfront = Circle('centerfront',1,2,isvanguard = True)
        self.rightback = Circle('rightback',2,1)
        self.leftback = Circle('leftback',2,3)
        self.centerback = Circle('centerback',2,2)
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
        
        
    def deck_init(self):
        self.deckzone.cardlist = []
        for i in self.decklist:
            if self.decklist[i] == -1:
                self.firstvan = Gamecard(i)
            else:
                for n in range(self.decklist[i]):
                    self.deckzone.cardlist.append(Gamecard(i))
        shuffle(self.deckzone.cardlist)
    
    def set_firstvan(self):
        self.centerfront.call_card(self.firstvan)
        
        
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