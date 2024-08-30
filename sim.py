### chap11/sim.py -- Self-avoiding random walk simulation
import sys
from city import CitySqGrid
import dogwalk

def sim(blocks, trials, verbose):
    # Initialize the metric of interest
    dead_ends = 0

    # Build the specified city
    my_city = CitySqGrid(blocks, dogwalk.Cosmo)
    if verbose:
        print(f'\nBuilding a {blocks}x{blocks} city')
        print(my_city)

    for _ in range(trials):
        # Reset the city before each trial
        my_city.reset()

        # Run, record, and print the trial
        success = dogwalk.dogwalk(my_city)
        if not success:
            dead_ends += 1
        if verbose:
            print(my_city)

    # Print the percentage of trials ending in dead ends
    print(f'{100 * dead_ends // trials}% dead ends')

def main():
    # Execution defaults
    verbose = False

    if len(sys.argv) == 4:
        verbose = True   # Anything in the verbose field works
    elif len(sys.argv) != 3:
        sys.exit("Usage: python3 sim.py blocks trials [verbose]")

    # Process the remaining command line arguments
    blocks = int(sys.argv[1])  # on a side of the square grid; try 4
    trials = int(sys.argv[2])  # number of simulation runs; try 20

    sim(blocks, trials, verbose)

if __name__ == '__main__':
    main()