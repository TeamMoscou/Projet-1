import test
#import test1
import test_Lidar_Detection_Thread

instance = test_Lidar_Detection_Thread
#instance1 = test1

lidar_thread = instance.LidarDetection()
#thrd1 = instance1.clock()
#test.cls()
#thrd.start()
lidar_thread.start()