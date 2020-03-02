from romipi_astar.romipi_driver import AStar
import time
import PyLidar3
import math
import asyncio

romi = AStar()

speed = 0.2  # speed in m/s
direction = 0.0 # direction in radians
longest = 0
longest_angle = 0
linear_ms = 0.0
rotate_rads = 0.0
bintotal = 37  # how many bins there are
x=[]
y=[]
bins=[]
for _ in range(360):
    x.append(0)
    y.append(0)
for _ in range (bintotal):  # clear the bins
    bins.append(0)
port = "/dev/ttyUSB0" #linux
Obj = PyLidar3.YdLidarX4(port) #PyLidar3.your_version_of_lidar(port,chunk_size)
loop = asyncio.get_event_loop()

async def motors():
    while True:
        romi.twist(speed, direction)
        await asyncio.sleep(0)

async def main():
    global speed, direction
    t = time.time() # start time
    while True:
        data = next(gen)
        longest = 0
        longest_bin = 0
        counter = 1
        for bin_num in range (bintotal):  # clear the bins
            bins[bin_num] = 0
        bin_num = 0
        for angle in range(0,360):
            if(data[angle]> 0):
                if counter < 10:
                    bins[bin_num] = bins[bin_num] + data[angle]
                    counter = counter + 1
                else:
                    bins[bin_num] = bins[bin_num] + data[angle]
                    bin_num = bin_num +1
                    counter = 1
        for bin_num in range(bintotal):
            if bins[bin_num] > longest:
                longest = bins[bin_num]
                longest_bin = bin_num
        longest = round(longest/1000,1)

        left_total = 0
        right_total = 0
        for x in range(0,longest_bin-1): # sum the left side
            left_total = left_total + bins[x]
        left_average = round((left_total/(longest_bin-1))/1000,1)

        for x in range(longest_bin+1,bintotal): # sum the right side
            right_total = right_total + bins[x]
        right_average = round((right_total/(bintotal-(longest_bin+1)))/1000,1)

        print("Longest range",longest)
        print("Left average", left_average)
        print("Right average", right_average)
        if left_average > right_average:
            furthest_side_dist = left_average
        else:
            furthest_side_dist = right_average

        print("longest bin #", longest_bin)
        bias = (longest-furthest_side_dist)*0.1
        print("Bias: ", bias)
        direction = longest_bin + bias
        print("Adjusted direction", direction)
        direction = round(math.radians((longest_bin*10)-180),2)
        print ("Steer:", direction)
        await asyncio.sleep(0.3)

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
