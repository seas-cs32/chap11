### chap11/directions0.py -- Finding driving directions (first try)
import maze

# Marks for map, which use color codes for terminal printing
EXPLORED = '\033[34m*\033[0m' # blue *
FRONTIER = '\033[32mf\033[0m' # green f

def search(my_map):
    g = my_map.grid
    frontier = []

    loc = my_map.start
    row, col = loc
    g[row][col].content = EXPLORED

    while loc != my_map.goal:
        # Build list of unexplored locations. A move is possible if there's not
        # a wall in that direction. We also add unexplored locations only once.
        if not g[row][col].northwall and \
            g[row-1][col].content != EXPLORED and \
            (row-1,col) not in frontier:
            frontier.append((row-1, col))
            g[row-1][col].content = FRONTIER
        if not g[row][col].southwall and \
            g[row+1][col].content != EXPLORED and \
            (row+1,col) not in frontier:
            frontier.append((row+1, col))
            g[row+1][col].content = FRONTIER
        if not g[row][col].eastwall and \
            g[row][col+1].content != EXPLORED and \
            (row,col+1) not in frontier:
            frontier.append((row, col+1))
            g[row][col+1].content = FRONTIER
        if not g[row][col].westwall and \
            g[row][col-1].content != EXPLORED and \
            (row,col-1) not in frontier:
            frontier.append((row, col-1))
            g[row][col-1].content = FRONTIER

        # my_map.print() # uncomment to see the frontier grow

        if len(frontier) == 0:
            print('No solution')
            return

        # Choose a location from the frontier as next to explore
        loc = frontier.pop()
        row, col = loc
        g[row][col].content = EXPLORED

    print('Found a solution')
    my_map.print()
    return


def main():
    print('\nBuilding our map')
    my_map = maze.Maze(maze.MAZE_map, maze.MAZE_map_endpts)
    my_map.print()

    print('Starting the search')
    search(my_map)

if __name__ == '__main__':
    main()