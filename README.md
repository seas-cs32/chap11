This directory contains everything needed for
**Chapter 11 (Discover Driving Directions)** in
[*Computational Thinking and Problem Solving (CTPS)*](https://profsmith89.github.io/ctps/ctps.html)
by Michael D. Smith.

`pin.py`: Definition of our Pin data type. Run by itself, it runs some tests.

`maze.py`: Definition of our Maze data type. Run by itself, it runs some tests.

`city.py`: Definition of the CitySqGrid data type. Run by itself, it runs some
tests.

`walk.py`: A simple script that allows us to direct a walk around a city.

`dogwalk.py`: An implementation of a self-avoiding random walk.

`sim.py`: An implementation of a self-avoiding random walk simulation that
invokes `dogwalk` on a specified square-grid city for a specified number
of trials.

`wander.py`: A version of `dogwalk.py` with pins in the city map.

`directions0.py`: A first start at actual driving directions.

`directions-dfs.py`: A depth-first-search (dfs) approach that produces driving
directions.

`directions-bfs.py`: A breadth-first-search (bfs) approach that produces
directions that take the shortest path from start to goal.
