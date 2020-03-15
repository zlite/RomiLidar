from romipi_astar.romipi_driver import AStar
import time
import PyLidar3
import math


romi = AStar()

speed = 0.2  # speed in m/s
direction = 0.0 # direction in radians
increment_turn = 0.5
bins=[]
for _ in range (360):  # clear the bins
    bins.append(0)
port = "/dev/ttyUSB0" #linux
Obj = PyLidar3.YdLidarX4(port) #PyLidar3.your_version_of_lidar(port,chunk_size)


def main():
    global direction
    while True:
        data = next(gen)
        left_total = 0
        right_total = 0
        center_total = 0
        for angle in range(340,20):  # measure the center
            if(data[angle]> 0):
                center_total = center_total + data[angle]
        center_average = round(center_total/40000,2)
        for angle in range(20,120):  # measure the right side
            if(data[angle]> 0):
                right_total = right_total + data[angle]
        right_average = round(right_total/120000,2)
        for angle in range(240,340): # measure the left side
            if(data[angle]> 0):
                left_total = left_total + data[angle]
        left_average = round(left_total/120000,2)
        print("Center average", center_average)
        print("Left average", left_average)
        print("Right average", right_average)
        if (center_average > right_average) and (center_average > left_average):
            direction = 0
        if (left_average > right_average) and (left_average > center_average):
            direction = round(direction + (increment_turn*(left_average-right_average)),2)
        if (right_average > left_average) and (right_average > center_average):
            direction = round(direction - (increment_turn*(right_average-left_average)),2)
        if direction > math.pi: direction = math.pi  # avoid overturning
        if direction < -math.pi: direction = -math.pi
        print ("Steer", direction)
        romi.twist(speed, direction)
        romi.twist(speed,0) #go straight
        time.sleep (0.5)



try:
    if(Obj.Connect()):
        print(Obj.GetDeviceInfo())
        gen = Obj.StartScanning()
    else:
        print("Error connecting to device")
    main()
except (KeyboardInterrupt, SystemExit):
    print("Quitting")
    Obj.StopScanning()
    Obj.Disconnect()
