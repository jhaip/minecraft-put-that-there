"""
Mines a set of stairs 2 blocks wide going down in whatever direction the bot
is facing when it starts.
"""

from botchallenge import *

def mine_if_solid(robot, direction):
    """Mines the block only if it's a solid block (won't mine torches away)."""
    is_solid = robot.is_block_solid(direction)
    if is_solid:
        robot.mine(direction)

def mine_tunnel(robot):
    print("*** STARTING MINE_TUNNEL SCRIPT")
    for i in range(10):
        # Clear space above and below
        mine_if_solid(Dir.DOWN)
        mine_if_solid(Dir.UP)
        
        # Mine and move right
        mine_if_solid(Dir.RIGHT)
        robot.move(Dir.RIGHT)

        # Clear space above and below
        mine_if_solid(Dir.DOWN)
        mine_if_solid(Dir.UP)
        
        # Move left + down + forward
        mine_if_solid(Dir.LEFT)
        robot.move(Dir.LEFT)
        mine_if_solid(Dir.DOWN)
        robot.move(Dir.DOWN)
        mine_if_solid(Dir.FORWARD)
        robot.move(Dir.FORWARD)
    robot.message_all("Tunnel complete!")
    print("done!")
