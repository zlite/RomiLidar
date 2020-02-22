from romipi_astar.romipi_driver import AStar
import time
speed = 0.1
direction = 0
romi = AStar()

while True:
    romi.twist(speed, direction)
