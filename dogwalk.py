### chap11/dogwalk.py -- Self-avoiding random walk simulation
from city import CitySqGrid
import random

# Our faithful dog
Cosmo = '\N{DOG FACE}'

def sim(my_city, trials=1):
    """Runs {trials} trials of a self-avoiding random walk in {my_city}.  It
       returns the number of times the dog hit a dead end."""
    dead_ends = 0
    cg = my_city.grid

    for t in range(trials):
        loc = my_city.start
        row, col = loc
        my_city.reset()

        while loc in my_city:
            # Leave a scent at current loc
            cg[row][col].content = '*'

            # Build list of available moves.  A move is available if there's not
            # a wall in that direction and no scent there.
            moves = []
            if not cg[row][col].northwall and cg[row-1][col].content != '*':
                moves.append('n')
            if not cg[row][col].southwall and cg[row+1][col].content != '*':
                moves.append('s')
            if not cg[row][col].eastwall and cg[row][col+1].content != '*':
                moves.append('e')
            if not cg[row][col].westwall and cg[row][col-1].content != '*':
                moves.append('w')

            #print(f'DEBUG: t = {t}; loc = {loc}; moves = {moves}')

            if len(moves) == 0:
                dead_ends += 1
                break

            # Move to a random available choice
            m = random.choice(moves)
            if m == 'n':
                row -= 1
            if m == 's':
                row += 1
            if m == 'e':
                col += 1
            if m == 'w':
                col -= 1
            cg[row][col].content = Cosmo
            loc = (row, col)

        print(my_city)

    return dead_ends


def main():
    print('\nBuilding a city with a square grid pattern')
    not_Boston = CitySqGrid(4, Cosmo)
    print(not_Boston)

    # Uncomment lines 71-75 if you want to see one random
    # walk, or lines 78-80 if you want to run a random-walk
    # simulation.

    # Cosmo walks himself
    dead_ends = sim(not_Boston)
    if dead_ends == 1:
        print(f'Cosmo hit a dead-end.')
    else:
        print(f'Cosmo is frolicing in the fields!')

    # Run a self-avoiding random walk simulation
    # trials = 20
    # dead_ends = sim(not_Boston, trials)
    # print(f'{100 * dead_ends // trials}% dead ends')

if __name__ == '__main__':
    main()