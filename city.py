### chap11/city.py
import maze

class CitySqGrid(maze.Maze):
    """Abstraction: A CitySqGrid object represents a grid-like layout of a city
       with an even number of blocks in the north-south direction as it has in
       the east-west direction.  When an instance is created, your character is
       placed at the intersection in the exact center of the city.

       Interface attributes:

       instance.start: Starting location for your character in the your city.
       Locations are (row,col) tuples that specify a coordinate within the city
       grid.  You should only read this data attribute.

       instance.grid: A 2-dimensional array of cells containing information
       about the city grid and whatever you might find at each cell.  Locations
       index the cells in a grid.  See class `Cell` for more information about
       the city cells.

       instance.move(location, direction): Given a location and a direction to
       move, this method moves the contents of the input location to the new
       location in the specified direction, if the direction doesn't hit a wall.
       If direction is a wall, no move is made.  NOTE: It is up to the caller to
       guarantee that there's some character to move at location and that the
       input location is within the city grid.

       instance.reset(): Resets all the city's state to the state when this
       instance was first created.

       instance.__contains__(pt): Allows us to use the Python `in` syntax to
       check if a location `pt` is a location in your city grid.

       instance.__str__(): Converts your city object into a string, which when
       printed is an ASCII representation of what your city looks like.

       instance.print(): Same as `__str__`, except that it does the print too.
    """
    # Implementation details:  It only builds cities where there is an
    # intersection at the exact middle of the city.  This means that the
    # CitySqGrid size must be an even number.  For more implementation details,
    # see class `Maze`, on which we build this class.

    def __init__(self, size, character='s'):
        # Initializes the instance as a {size}-by-{size} maze object and sets
        # the start-point character to {character}

        # Sanity checks
        if size & 0x1 != 0:
            assert('CitySqGrid size must be an even number')
        if size < 2 or size > 20:
            assert('CitySqGrid size must be between 2 and 20 buildings')

        # Create the string that describes the configuration.  The actual
        # configuration written out is one of the test cases in maze.py.
        row1 = 'f5' * (size - 1) + 'f\n'
        row2 = 'a0' * (size - 1) + 'a\n'
        # Finally, put it all together with no trailing newline
        config = (row1 + row2) * (size - 1) + row1[0:-1]
        #DEBUG print(config)

        # Put start in city center, which is just the point (size,size)
        # when we double size to make maze rows and columns!  We don't
        # care about the goal point in this application.
        endpts = f'({size},{size}) (-1,-1)'
        #DEBUG print(endpts)
        
        maze.Maze.__init__(self, config, endpts)

        # Fill in the buildings.  Only seen on first build.  maze.reset
        # won't refill these buildings, which is the desired behavior
        # once we start the dog on its random walk.
        for i in range(1, size * 2, 2):
            for j in range(1, size * 2, 2):
                self.grid[i][j].content = '#'

        # Change 's' to a dog
        self.grid[size][size].content = character


def main():
    # Just a testing routine

    cosmo = '\N{DOG FACE}'

    print('\nBuilding a small city grid')
    city = CitySqGrid(4)
    city.print()

    print('\nPrinting it again with print()')
    print(city)

    print('\nBuilding a small city grid with Cosmo')
    city = CitySqGrid(4, cosmo)
    city.print()

    print('\nBuilding a large city grid')
    city = CitySqGrid(16, cosmo)
    city.print()

if __name__ == '__main__':
    main()