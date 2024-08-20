### chap11/pin.py
import math

# Define useful pin icons and constants
green_heart = '\u001b[32m\u2665\u001b[0m'
red_x = '\u001b[31m\u2716\u001b[0m'
MAX_DISTANCE = 100.0

class Pin(object):
    """Abstraction: A Pin object is a mark at a map location `loc`
       with a `name`, descriptive `note`, and a ranking of 0-5 `stars`.
       These names are all instance attributes.

       instance.icon: The pins displayed icon, which depends upon
       the pin's number of `stars`.

       distance(location): Given a (x,y) location, this method
       computes and returns the as-the-crow-flies distance from it
       to this pin's location, but only if this pin is highly rated.

       __str__(): Converts the pin into a string.
    """
    def __init__(self, loc, name, note, stars):
        self.loc = loc
        self.name = name
        self.note = note

        assert stars >=0 and stars <=5, "Invalid number of stars"
        self.stars = stars

        if self.stars >= 3:
            self.icon = green_heart
        else:
            self.icon = red_x

    def __str__(self):
        return f"{self.name} at {self.loc} rated {self.stars}" + '\u2605'

    def distance(self, loc):
        if self.stars >= 3:
            return abs(math.dist(self.loc,loc))
        else:
            return MAX_DISTANCE


# Test the implementation of Pin using CitySqGrid
from city import CitySqGrid

def main():
    # Our faithful dog
    Cosmo = '\N{DOG FACE}'

    # Build a city
    nyc = CitySqGrid(6, Cosmo)

    # Create some pins and keep track of them in a list
    pins = [
        Pin((1,3), "Park", "Lots of squirrels", 5),
        Pin((3,7), "Fire Hydrant", "Many good smells", 4),
        Pin((9,5), "Cat", "Not a nice cat!", 1),
    ]

    # Add each pin in pins to the city map
    for pin in pins:
        print(f'Adding {pin}')
        nyc.mark(pin.loc, pin.icon)

    print(nyc)

    # Add a new pin
    new_pin = Pin((11,9), "Bakery", "Free dog treats!", 5)
    pins.append(new_pin)
    nyc.mark(new_pin.loc, new_pin.icon)
    print(f'Added {new_pin}')

    print(nyc)

    # Compute distances to the first two pins
    pin0, pin1 = pins[0], pins[1]
    dist = pin0.distance(nyc.start)
    print(f"Pin {pin0.loc} is {dist} units away")
    dist = pin1.distance(nyc.start)
    print(f"Pin {pin1.loc} is {dist} units away")

if __name__ == '__main__':
    main()
