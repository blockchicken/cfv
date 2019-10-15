

### Turn Order ###

### Draw Phase ###
phase = 'Draw'
draw(1)

### Stand Phase ###
phase = 'Stand'
for i in field:
    if i.card:
        i.card.isrest = False

### Ride Phase ###
phase = 'Ride'
# G-assist Logic

# g_assist()

# Ride Logic

### Stride Phase ###
phase = 'Stride'
# Stride Phase Logic
# later addition

### Main Phase ###
phase = 'Main'
# Main Phase Logic

### Battle Phase ###
phase = 'Battle'
# Battle Phase Logic

### End Phase ###
phase = 'End'
# change turns
