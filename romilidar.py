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
x=[]
y=[]
bins=[]
for _ in range(360):
    x.append(0)
    y.append(0)
for _ in range (37):  # clear the bins
    bins.append(0)
port = "/dev/ttyUSB0" #linux
Obj = PyLidar3.YdLidarX4(port) #PyLidar3.your_version_of_lidar(port,chunk_size)

async def motors(speed, direction):
    await romi.twist(speed, direction)

async def main:
    if(Obj.Connect()):
            print(Obj.GetDeviceInfo())
            gen = Obj.StartScanning()
            t = time.time() # start time
            while True:
                data = next(gen)
                longest = 0
                longest_bin = 0
                counter = 1
                for bin_num in range (37):  # clear the bins
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
                for bin_num in range(37):
                    if bins[bin_num] > longest:
                        longest = bins[bin_num]
                        longest_bin = bin_num
                print("longest range bin, bin #", round(longest/1000,0), longest_bin)
                direction = round(math.radians((longest_bin*10)-180),2)
                print ("Direction:", direction)
    else:
        print("Error connecting to device")

try:
    loop.run_until_complete(
        main()
        )
except (KeyboardInterrupt, SystemExit):
    print("Quitting")
    Obj.StopScanning()
    Obj.Disconnect()
