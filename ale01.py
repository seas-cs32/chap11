### chap11/ale01.py
import sys

green_heart = '\u001b[32m\u2665\u001b[0m'
red_x = '\u001b[31m\u2716\u001b[0m'

def make_3_pins(print_the_pins=False):
    # Create Cosmo's initial three pins
    pin1 = {
        "loc" : (3,11), 
        "name" : "Park", 
        "note" : "Lots of good squirrels", 
        "stars" : 5,
    }
    pin2 = {
        "loc" : (7,9),
        "name" : "Fire Hydrant",
        "note" : "Many good smells",
        "stars" : 4,
    }
    pin3 = {
        "loc" : (5,3),
        "name" : "Cat",
        "note" : "Not a nice cat!",
        "stars" : 1,
    }

    if print_the_pins:
        # Print the name field of the created pins
        pass
        # INSERT STEP 1 SOLUTION CODE HERE

    # INSERT STEP 2 SOLUTION CODE HERE


def set_pin_icon(pin):
    pass
    # INSERT STEP 7 SOLUTION CODE HERE


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 ale01.py STEP_NUMBER")
    else:
        step_num = int(sys.argv[1])
    
    print('\n** STEP 1 **')
    make_3_pins(step_num == 1)

    print('\n** STEP 2 **')
    if step_num >= 2:
        pins = make_3_pins()
        if step_num == 2:
            print(pins)

    print('\n** STEP 3 **')
    if step_num == 3:
        pass
        # INSERT STEP 3 SOLUTION CODE HERE

    print('\n** STEP 4 **')
    if step_num == 4:
        pass
        # INSERT STEP 4 SOLUTION CODE HERE

    if step_num >= 6:
        pass
        # INSERT STEP 6 SOLUTION CODE HERE
    
    print(f'\n** STEP(s) {[s for s in range(5,step_num+1)]} **')
    if step_num == 5 or step_num == 6:
        pass
        # INSERT STEP 5 SOLUTION CODE HERE

    print('\n** STEP 7 **')
    if step_num == 7:
        for loc in pins:
            set_pin_icon(pins[loc])
            print(f'Pin at {loc} gets icon {pins[loc]["icon"]}')
    
    print()

if __name__ == '__main__':
    main()
