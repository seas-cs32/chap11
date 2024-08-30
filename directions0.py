### chap11/directions0.py -- Finding driving directions (first try)
import maze

# Marks for map, which use color codes for terminal printing
EXPLORED = '\033[34m*\033[0m' # blue *
FRONTIER = '\033[32mf\033[0m' # green f

def search(my_map):
    # Set the current state and mark the map location explored
    cur_loc = my_map.start
    my_map.mark(cur_loc, EXPLORED)

    # Build a list on which to keep known but unexplored locations
    frontier = []

    while cur_loc != my_map.goal:    # search loop
        # What unexplored next steps are possible?
        moves = my_map.possible_moves(cur_loc, EXPLORED)

        # Add moves not already on the frontier to the frontier
        for a_move in moves:
            loc = my_map.simulate_move(cur_loc, a_move)
            if loc not in frontier:
                frontier.append(loc)
                my_map.mark(loc, FRONTIER)

        # DEBUG: Uncomment to watch the frontier grow
        # print(my_map)
        # print(f'DEBUG: cur_loc = {cur_loc}; moves = {moves}')
        # print(f'frontier = {frontier}')
        # input('Ready to move on? ')

        if len(frontier) == 0:
            print('No solution')
            return

        # Choose a location from the frontier as next to explore
        next_loc = frontier.pop()
        my_map.mark(next_loc, EXPLORED)

        # Update current state
        cur_loc = next_loc

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