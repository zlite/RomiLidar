from romipi_astar.romipi_driver import AStar
import time
import PyLidar3
import math
import threading


romi = AStar()

speed = 0.2  # speed in m/s
direction = 0.0 # direction in radians
increment_turn = 0.5
bins=[]
for _ in range (360):  # clear the bins
    bins.append(0)
port = "/dev/ttyUSB0" #linux
Obj = PyLidar3.YdLidarX4(port) #PyLidar3.your_version_of_lidar(port,chunk_size)


def drive():
    while True:
        romi.twist(speed, direction)
        time.sleep(0.2)


def main():
    global direction
    while True:
        data = next(gen)
        left_total = 0
        right_total = 0
        center_total = 0
        bias = 0
        for angle in range(340,360):  # measure the center
            if(data[angle]> 0):
                center_total = center_total + data[angle]
        for angle in range(0,20):  # measure the center
            if(data[angle]> 0):
                center_total = center_total + data[angle]
        center_average = round(center_total/40,2)
        for angle in range(20,120):  # measure the right side
            if(data[angle]> 0):
                right_total = right_total + data[angle]
        right_average = round(right_total/120,2)
        for angle in range(240,340): # measure the left side
            if(data[angle]> 0):
                left_total = left_total + data[angle]
        left_average = round(left_total/120,2)
        print("Center average", center_average)
        print("Left average", left_average)
        print("Right average", right_average)
        difference = (left_average - right_average)/1000
        if (center_average > right_average) and (center_average > left_average): # forward is clearer
            if left_average < 150: # too close to left wall
                bias = -0.4
            if right_average < 150: # too close to right wall
                bias = 0.4
            direction = 0 + bias
        if (left_average > right_average) and (left_average > center_average):
            direction = round(direction + (increment_turn*(difference)),2)
        if (right_average > left_average) and (right_average > center_average):
            direction = round(direction - (increment_turn*(-1*difference)),2)
        if direction > math.pi: direction = math.pi  # avoid overturning
        if direction < -math.pi: direction = -math.pi
        print ("Steer", direction)

try:
    if(Obj.Connect()):
        print(Obj.GetDeviceInfo())
        gen = Obj.StartScanning()
        threading.Thread(target=drive).start()
    else:
        print("Error connecting to device")
    main()
except (KeyboardInterrupt, SystemExit):
    print("Quitting")
    Obj.StopScanning()
    Obj.Disconnect()
