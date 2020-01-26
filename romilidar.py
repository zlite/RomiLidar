from romipi_astar.romipi_driver import AStar
import time
import PyLidar3

romi = AStar()
linear_ms = 0.0
rotate_rads = 0.0


port = "/dev/ttyUSB0" #linux
Obj = PyLidar3.YdLidarX4(port) #PyLidar3.your_version_of_lidar(port,chunk_size)

if(Obj.Connect()):
    print(Obj.GetDeviceInfo())
    gen = Obj.StartScanning()
    t = time.time() # start time
    while True: 
        data = next(gen)
        for angle in range(0,360):
            if(data[angle]>1000):
                x[angle] = data[angle] * math.cos(math.radians(angle))
                y[angle] = data[angle] * math.sin(math.radians(angle))
    Obj.StopScanning()
    Obj.Disconnect()
else:
    print("Error connecting to device")
