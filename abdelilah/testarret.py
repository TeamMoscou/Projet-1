# coding: utf-8
from rplidar import RPLidar


if __name__ == "__main__":

    #lidar instance
    lidar = RPLidar('/dev/ttyUSB0')
    lidar.stop()
    lidar.disconnect()
    
    #lidar.reset()
   




