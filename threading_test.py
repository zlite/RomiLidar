import threading
import PyLidar3
import math
import time
from romipi_astar.romipi_driver import AStar

romi = AStar()

speed = 0.2  # speed in m/s
direction = 0.0 # direction in radians

def drive():
    while True:
        romi.twist(speed, 0)


x=[]
y=[]
for _ in range(360):
    x.append(0)
    y.append(0)

port = "/dev/ttyUSB0" #linux
Obj = PyLidar3.YdLidarX4(port)  #PyLidar3.your_version_of_lidar(port,chunk_size)
threading.Thread(target=drive).start()
if(Obj.Connect()):
    print(Obj.GetDeviceInfo())
    gen = Obj.StartScanning()
    t = time.time() # start time
    while (time.time() - t) < 10: #scan for 30 seconds
        data = next(gen)
        print("got new data")
        for angle in range(0,360):
            if(data[angle]>1000):
                x[angle] = data[angle] * math.cos(math.radians(angle))
                y[angle] = data[angle] * math.sin(math.radians(angle))
    Obj.StopScanning()
    Obj.Disconnect()
else:
    print("Error connecting to device")
