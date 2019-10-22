### Turn Order ###

#if turncount == 0, both players mulligan
#activeplayer = nextplayer(), something like this to keep track of turn player
#turncount += 1

### Draw Phase ###

skilltime = 1 #Start of Turn
# Begin Cont skills active during player turn

skilltime = 2 #Draw

### Stand Phase ###

skilltime = 3 #Prior to standing

### Ride Phase ###

skilltime = 4 #Start of Ride Phase

# G Assist Check
# G Assist Performance

skilltime = 5 #When Ridden Upon

### Stride Phase ###

# Blank for now

### Main Phase ###

skilltime = 6 #Start of Main Phase
# For skills specifically when Main Phase starts

skilltime = 7 #During Main Phase - Player can enter battle phase or take any of the following actions:
# Allow player to call cards from hand to field, swap columns, provide list to player of all possible act abilities that can pay their current costs

skilltime = 8 #End of Main Phase
# For skills specifically when Main Phase ends

### Battle Phase ###

skilltime = 9 # Start of Battle Phase

skilltime = 10 #Select Attacking Column, Defending Unit, Boost, Blaze

skilltime = 11 #When This Unit declares an attack and in Attacking circle, When this unit Boosts behind Attacking circle

skilltime = 12 #Guard Step, Select Guardians, Call Guardians, Intercept, use Protect/Sentinel skills when placed or while on Guardian Circle

skilltime = 13 #Damage Calculation, check active total power, compare to opponent unit's active total power. If >=, hits, else next

skilltime = 14 #Damage Check

skilltime = 15 #When placed in Damage Zone

skilltime = 16 #When sent to dropzone from Guardian circle, when retired from field

skilltime = 17 #When unit hits skills

skilltime = 18 #After this unit attacks skills

# Battle loop, return to Selecting Attacking Column or ending turn.

### End Phase ###

skilltime = 19 #Start of End Phase

skilltime = 20 #End of turn, Retire any units that are temporary, 
# end_of_turn() - generic end of turn procedure, returning boosted power back to normal

### 