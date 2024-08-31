### chap11/wander.py -- Wander through the city's highlights
from maze import NO_LOC
from city import CitySqGrid
from pin import Pin, MAX_DISTANCE

# Our faithful dog
Cosmo = '\N{DOG FACE}'

# Command encoding
commands = [
    'n',  # step north
    'e',  # step east
    'w',  # step west
    's',  # step south
    'c',  # jump to the closest highly-rated pin
    'q',  # quit
]

def wander(my_city, pins):
    cur_loc = my_city.start

    while cur_loc in my_city:    # wander only in the city
        answer = input('Where to? ')
        if answer == '':
            continue             # handle no answer gracefully
        cmd = answer[0].lower()  # use only the first letter

        if cmd not in commands:
            print(f"Unknown command. Use {commands}")
            continue

        elif cmd == 'q':
            return
        
        elif cmd == 'c':
            best_loc = NO_LOC            # not a valid location
            best_distance = MAX_DISTANCE # bigger than any allowable map

            # Find the closest highly-rated pin
            for pin in pins:
                dist = pin.distance(cur_loc)
                if dist < best_distance:
                    best_loc = pin.loc
                    best_distance = dist

            assert best_loc != NO_LOC, "Failed to find a pin"

            # Teleport to within one step, which requires me to erase
            # the character from the cur_loc.
            character = my_city.get_mark(cur_loc)
            my_city.mark(cur_loc, ' ')
            cur_loc = (best_loc[0] - 1, best_loc[1] - 1)
            my_city.mark(cur_loc, character)
            direction = 'n'

        else:
            direction = cmd

        # Make the move and show the updated map
        cur_loc = my_city.move(cur_loc, direction)
        print(my_city)

def main():
    # Build the city and put Cosmo at its center
    nyc = CitySqGrid(6, Cosmo)

    # Add Cosmo's favorite pins to the city map
    pins = [
        Pin((3,11), "Park", "Lots of squirrels", 5),
        Pin((7,9), "Fire Hydrant", "Many good smells", 4),
        Pin((5,3), "Cat", "Not a nice cat!", 1),
        Pin((9,1), "Bakery", "Free dog treats!", 5)
    ]
    for pin in pins:
        nyc.mark(pin.loc, pin.icon)

    print(nyc)

    wander(nyc, pins)

    print('Thanks for the fun walk!')

if __name__ == '__main__':
    main()
