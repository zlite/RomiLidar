from romipi_astar.romipi_driver import AStar
import time
import PyLidar3
import math
import threading


romi = AStar()

speed = 0.2  # speed in m/s
direction = 0.0 # direction in radians
increment_turn = 0.4
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
        for angle in range(20,100):  # measure the right side
            if(data[angle]> 0):
                right_total = right_total + data[angle]
        right_average = round(right_total/80,2)
        for angle in range(260,340): # measure the left side
            if(data[angle]> 0):
                left_total = left_total + data[angle]
        left_average = round(left_total/80,2)
        print("Center average", center_average)
        print("Left average", left_average)
        print("Right average", right_average)
        left_y = math.sin(math.pi/4) * left_average
        left_x = -1*math.cos(math.pi/4) * left_average
        right_y = math.sin(math.pi/4) * right_average
        right_x = math.cos(math.pi/4) * right_average
        center_y = center_average

        sum_x = round(left_x + right_x,2)
        sum_y = round(center_y - (left_y + right_y)/2,2)
        if sum_y < 100:
            sum_y = 100
        print("Sum x:", sum_x, "Sum y: ", sum_y)
        sum_angle = math.atan2(sum_x,sum_y)
        print ("Sum Steer", round(sum_angle,2))
        direction = -1* sum_angle
        sum_dist = math.sqrt(sum_x**2 + sum_y**2)


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
