### chap11/dogwalk.py -- Self-avoiding random dog walk
from city import CitySqGrid
import random

# Our faithful dog and the scent he smells
Cosmo = '\N{DOG FACE}'
EXPLORED = '\033[34m*\033[0m' # blue *

def dogwalk(my_city):
    """Given a city of type CitySqGrid, take a random walk
       and return True if goal successfully met. The
       successful path is marked in the city object."""
    # Set the current state
    cur_loc = my_city.start

    while cur_loc in my_city:
        # Where to? Well, what steps are possible?
        moves = my_city.possible_moves(cur_loc, EXPLORED)
        # print(f'DEBUG: loc = {loc}; moves = {moves}')

        if len(moves) == 0:
            return False   # dead end!

        # Randomly pick a possible move and make it
        a_move = random.choice(moves)
        next_loc = my_city.move(cur_loc, a_move)

        # Leave a scent at current loc
        my_city.mark(cur_loc, EXPLORED)

        # Update current state
        cur_loc = next_loc

    # The random path was successful!
    return True

def main():
    print('\nBuilding a city with a 4x4 square grid')
    nyc = CitySqGrid(4, Cosmo)
    print(nyc)

    # Cosmo walks himself
    success = dogwalk(nyc)
    print(nyc)
    if success:
        print(f'Cosmo is frolicing in the fields!')
    else:
        print(f'Cosmo hit a dead-end.')

if __name__ == '__main__':
    main()