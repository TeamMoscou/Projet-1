import Lidar_Detection_Thread
import interface
import Ultrason

lidar_instance = Lidar_Detection_Thread
interface_instance = interface
Ultrason_instance = Ultrason

lidar_thread = lidar_instance.LidarDetection()
interface_thread = interface_instance.Interface()
ultrason_thread = Ultrason_instance.Ultrason()

lidar_thread.start()
interface_thread.start()
ultrason_thread.start()