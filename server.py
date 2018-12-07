import Lidar_Detection_Thread
import interface

lidar_instance = Lidar_Detection_Thread
interface_instance = interface

lidar_thread = lidar_instance.LidarDetection()
interface_thread = interface_instance.Interface()

lidar_thread.start()
interface_thread.start()
