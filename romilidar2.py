from romipi_astar.romipi_driver import AStar
import time
import PyLidar3
import math
import asyncio

romi = AStar()

speed = 0.2  # speed in m/s
direction = 0.0 # direction in radians
increment_turn = 0.1
bins=[]
for _ in range (360):  # clear the bins
    bins.append(0)
port = "/dev/ttyUSB0" #linux
Obj = PyLidar3.YdLidarX4(port) #PyLidar3.your_version_of_lidar(port,chunk_size)
loop = asyncio.get_event_loop()

async def motors():
    while True:
        romi.twist(speed, direction)
        romi.twist(speed,0) #go straight
        await asyncio.sleep(0.2)

async def main():
    global direction
    while True:
        data = next(gen)
        left_total = 0
        right_total = 0
        for angle in range(0,90):  # measure the right side
            if(data[angle]> 0):
                right_total = right_total + data[angle]
        right_average = round(right_total/90,2)
        for angle in range(270,360): # measure the left side
            if(data[angle]> 0):
                left_total = left_total + data[angle]
        left_average = round(left_total/90,2)
        print("Left average", left_average)
        print("Right average", right_average)
        if left_average > right_average:
            direction = round(direction + increment_turn,2)
        else:
            direction = round(direction - increment_turn,2)
        print ("Steer", direction)
        await asyncio.sleep(0)

try:
    if(Obj.Connect()):
        print(Obj.GetDeviceInfo())
        gen = Obj.StartScanning()
    else:
        print("Error connecting to device")
    ioloop = asyncio.get_event_loop()
    tasks = [
        ioloop.create_task(main()),
        ioloop.create_task(motors())
        ]
    ioloop.run_until_complete(asyncio.wait(tasks))
    ioloop.close()
except (KeyboardInterrupt, SystemExit):
    print("Quitting")
    Obj.StopScanning()
    Obj.Disconnect()
