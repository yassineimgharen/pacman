# config json
Simple summary:

   Key	                    Unit	                        Controls
fps	                     frames/sec	                game speed / smoothness
cell_size	             pixels	                    how big the maze looks
level_max_time	         seconds	                time pressure per level
timeout_action	         string	                    what happens at timeout
frightened_duration	     seconds                    how long ghosts stay scared
ghost_respawn_delay	     seconds	                how long ghost stays dead


# maze.py

1- can_move → player and ghosts need to know if they can move in a direction before moving. Instead of doing bitmask math everywhere, they just call maze.can_move(x, y, dx, dy)
1- get_corners → when a level starts, you need to know where to place the 4 ghosts and 4 super-pacgums. Corners of the maze.
3- get_center → when a level starts, you need to know where to place the player. Center of the maze.

# 1 8 4 2

These are just the 4 possible bit positions in a 4-bit number:
bit 0 = 1  = 0001 in binary
bit 1 = 2  = 0010 in binary
bit 2 = 4  = 0100 in binary
bit 3 = 8  = 1000 in binary

The maze generator decided:

1 (0001) = North wall exist
2 (0010) = East wall exist
4 (0100) = South wall exist
8 (1000) = West wall exist


# can_move maze.py

can_move takes the current position (x, y) and a direction (dx, dy). First it calculates the target cell by adding dx and dy to the current position. Then it checks if that target cell is inside the grid — if not, return False (can't move outside the maze).

Then it checks the bitmask of the current cell. Each direction has a wall bit — North=1, East=2, South=4, West=8. It uses & to check if that specific bit is set in the cell's number. If the bit is 0 → no wall → you can move → return True. If the bit is not 0 → wall exists → you can't move → return False.

# fps
FPS = Frames Per Second. How many times the game loop runs per second

# Ghost states
CHASE → moving toward the player
FRIGHTENED → moving away from player (after super-pacgum eaten)
DEAD → eaten, waiting to respawn at its corner

# calculate move relation
1- find possibel moves
2- calculate distance using player position and possible move
3- chose smallest distance

example:
+--+--+--+--+--+
|  |           |
+  +  +--+--+  +
|     |     |  |
+--+--+  +  +  +      
|   G |  |    P|
+--+  +--+  +  +
|              |
+--+--+--+--+--+
Ghost G at (1,2), player P at (4,2)

From (1,2) valid directions:

North (0,-1) → wall ❌
East (1,0) → wall ❌
South (0,1) → open ✅ → (1,3) → distance = (1-4)²+(3-2)² = 9+1 = 10
West (-1,0) → open ✅ → (0,2) → distance = (0-4)²+(2-2)² = 16+0 = 16

Ghost picks South → smallest distance 10 → moves to (1,3).

ghost's new x minus player's x 
ghost's new y minus player's y

From (1,3) next frame → keeps calculating → eventually finds path to player through the corridor


# check if a wall open

North = 1 = 0001
East  = 2 = 0010
South = 4 = 0100
West  = 8 = 1000

Think of the cell value as 4 light switches, one per wall:

bit 3  bit 2  bit 1  bit 0
West   South  East   North

Copy
Cell value 9 = 1001 in binary means:

West=1  South=0  East=0  North=1
 ON      OFF      OFF     ON

Copy
→ West wall ON, North wall ON, East and South walls OFF.

To check if North wall exists, you check bit 0:

9 & 1 → is bit 0 ON?
1001
0001
----
0001 = 1 → ON → wall exists → can't move North

Copy
To check if East wall exists, you check bit 1:

9 & 2 → is bit 1 ON?
1001
0010
----
0000 = 0 → OFF → no wall → can move East