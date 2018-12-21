
if __name__ == "__main__":

    
    lidar_instance = test_lidar_detection_thread

    lidar_thread = lidar_instance.LidarDetection()

    lidar_thread.daemon = True
    
    
    lidar_thread.start()

    lidar_thread.join()
