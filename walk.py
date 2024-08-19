### chap11/walk.py -- A walk to escape the city
from city import CitySqGrid

# Our faithful dog
Cosmo = '\N{DOG FACE}'

# Build the city and put Cosmo at its center
nyc = CitySqGrid(4, Cosmo)
print(nyc)

# Loop that walks Cosmo
loc = nyc.start
while loc in nyc:
    direction = input('Where to? ')
    loc = nyc.move(loc, direction)
    print(nyc)

print('Enjoy your day outside the city!')
