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
offset = 0
increment_turn = 0.2
bintotal = 37  # how many bins there are
scale = 180/(bintotal/2)
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
        romi.twist(speed,0) #go straight
        await asyncio.sleep(0)

async def main():
    global speed, direction
    t = time.time() # start time
    while True:
        print ("Collecting data")
        data = next(gen)
        print ("got data")
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
        if (longest_bin-1) != 0:  # watch out for divide by zero
            left_average = round((left_total/(longest_bin-1))/1000,1)
        else:
            print ("divide by zero error!")
        for x in range(longest_bin+1,bintotal): # sum the right side
            right_total = right_total + bins[x]
        if (bintotal-(longest_bin+1)) != 0:  # watch out for divide by zero
            right_average = round((right_total/(bintotal-(longest_bin+1)))/1000,1)
        else:
            print ("divide by zero error!")

        print("Longest range",longest)
        print("Left average", left_average)
        print("Right average", right_average)
        if left_average > right_average:
            furthest_side_dist = left_average
        else:
            furthest_side_dist = right_average

        print("longest bin #", longest_bin)
        bias = round((longest-furthest_side_dist)*0.1,1)
        print("Bias: ", bias)
        temp_direction = longest_bin + bias
        print("Adjusted direction", temp_direction)
        temp_direction = round(math.radians(((longest_bin+bias)*scale)-180),2)
        print ("Open path direction:", temp_direction)
        if temp_direction < 0:
            direction = round(direction - increment_turn + offset,2)
        if temp_direction > 0:
            direction = round(direction + increment_turn + offset,2)
        print ("Steer", direction)
        # if temp_direction > 0:
        #     direction = temp_direction
        # else:
        #     print ("Negative direction", round(math.pi + temp_direction,2))
        #     direction = round(math.pi + temp_direction,2)
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
