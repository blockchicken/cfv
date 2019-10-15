# The core class, everything in the card game revolves around cards
class Card:
    def __init__(self, name, clan, nation, grade, power, shield, critical = 1,
    skill1 = None, skill2 = None, skill3 = None, marker = None, istrigger = False,
    triggertype = None, boost = False, intercept = False, drive = 1, flavor = None,
    image = None, tags = []):
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
        self.boost = boost
        self.intercept = intercept
        self.drive = drive
        self.flavor = flavor
        self.image = image
        self.tags = tags
    
    def get_name(self):
        return self.name
    
### Example Little_Sage_Marron = Card("Little Sage Marron","Royal Paladin","United Sanctuary",1,8000,10000, boost = True)

# Define Game Cards, Cards that will be used in the game

class Gamecard(Card):
    def __init__(self
                 , *args):
#                  ,name, clan, nation, grade, power, shield, critical
#                  ,skill1, skill2, skill3, marker, istrigger
#                  ,triggertype, boost, intercept, drive, flavor
#                  ,image, tags
#                  ,faceup = True, currentpower = 0, currentcritical = 1, currentdrive = 1, equipgauge = [], isrest = False, currentshield = 0):
#        Card.__init__(self, name, clan, nation, grade, power, shield, critical, skill1, skill2, skill3, marker, istrigger, triggertype, boost, intercept, drive, flavor, image, tags)
#         super(Gamecard, self).__init__()
        self.__dict__ = args[0].__dict__.copy()
        self.faceup = True
        self.currentpower = self.power
        self.currentcritical = self.critical
        self.currentdrive = self.drive
        self.equipgauge = []
        self.isrest = False
        self.currentshield = self.shield
    
    def counterblast(card):
        if self.faceup == True:
            self.faceup = False
        else:
            print('Error - Already Facedown')
    
    def countercharge(card):
        if self.faceup == False:
            self.faceup = True
        else:
            print('Error - Already Faceup')


# Define Circles


class Circle:
    def __init__(self, row, column, card = None, isaccel = False, marker = None, markercount = 0, isvanguard = False):
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

    def add_card(self,card):
        self.cardlist.append(card)
        
    def remove_card(self,card):
        self.cardlist.remove(card)
    
    def empty_list(self):
        self.cardlist = []
        


# Define Players


class Player:
    def __init__(self, name, decklist, clan = None, nation = None):
        self.name = name
        self.decklist = decklist
        self.clan = clan
        self.nation = nation