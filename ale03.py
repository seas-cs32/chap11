### chap11/ale03.py
import sys
from pin import Pin

class Pin2(Pin):
    def __init__(self, loc=(0,0), name='', note='', stars=0, pin=None):
        if pin:
            self.loc = pin.loc
            self.name = pin.name
            self.note = pin.note
            self.stars = pin.stars
            self.icon = pin.icon
        else:
            Pin.__init__(self, loc, name, note, stars)

    def __gt__(self, pin):
        return self.stars > pin.stars


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 ale03.py STEP_NUMBER")
    else:
        step_num = int(sys.argv[1])

    # Create some pins and keep track of them in a list
    pins = [
        Pin((3,11), "Park", "Lots of squirrels", 5),
        Pin((7,9), "Fire Hydrant", "Many good smells", 4),
        Pin((5,3), "Cat", "Not a nice cat!", 1),
        Pin((9,1), "Bakery", "Free dog treats!", 5),
    ]

    # Print them out
    print('** Original Pins **')
    for i in range(len(pins)):
        print(pins[i])
    print()

    # STEP 1
    if step_num == 1:
        print('Are the first and fourth pins equal?', pins[0] == pins[3])
        print('Is the first pin equal to itself?', pins[0] == pins[0])

    # STEP 2
    if step_num == 2:
        print('Is the first pin greater than the second one?', pins[0] > pins[1])

    # Create some new pins using the Pin subclass defined above
    pins2 = [Pin2(pin=pins[i]) for i in range(len(pins))]
    pin24 = Pin2((9,1), "Bakery", "Free dog treats!", 4)

    # Step 3
    if step_num >= 3:
        print('** New Pins2 **')
        for i in range(len(pins2)):
            print(pins2[i])
        print('pin24:', pin24)
        print()

    # Step 4
    if step_num == 4:
        print('Is the first subclassed pin greater than the second one?', pins2[0] > pins2[1])
        print('Is the third subclassed pin greater than the second one?', pins2[2] > pins2[1])

    # Step 5
    if step_num == 5:
        print('Are the first and fourth original pins equal?', pins[0] == pins[3])
        print('Are the first and fourth subclassed pins equal?', pins2[0] == pins2[3])

if __name__ == '__main__':
    main()
