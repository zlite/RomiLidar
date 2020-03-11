from romipi_astar.romipi_driver import AStar
import time
import math
import asyncio

romi = AStar()

speed = 0.2  # speed in m/s
direction = 0.0 # direction in radians
switch = False

async def motors():
    global direction
    while True:
        romi.twist(speed, direction)
        romi.twist(speed, 0)
        await asyncio.sleep(0)

async def main():
    global speed, direction, switch
    t = time.time() # start time
    # do bogus thing
    for i in range (1000):
        for j in range(1000):
            k = i*j

    while True:
        if direction < 1 and not switch:
            direction += 0.1
        else:
            switch = True
        if direction > 0 and switch:
            direction -= 0.1
        else:
            switch = False
        print("Direction", direction)
        await asyncio.sleep(0.3)

try:
    ioloop = asyncio.get_event_loop()
    tasks = [
        ioloop.create_task(main()),
        ioloop.create_task(motors())
        ]
    ioloop.run_until_complete(asyncio.wait(tasks))
    ioloop.close()
except (KeyboardInterrupt, SystemExit):
    print("Quitting")
