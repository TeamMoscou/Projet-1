import Lidar_Detection_Thread
import interface
import Ultrason


if __name__ == "__main__":

    print('Bring up CAN0....')
    os.system("sudo /sbin/ip link set can0 up type can bitrate 400000")
    time.sleep(0.1)

    try:
        bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
    except OSError:
        print('Cannot find PiCAN board.')
        exit()

    lidar_instance = Lidar_Detection_Thread
    interface_instance = interface
    Ultrason_instance = Ultrason

    lidar_thread = lidar_instance.LidarDetection()
    interface_thread = interface_instance.Interface()
    ultrason_thread = Ultrason_instance.Ultrason(bus)

    lidar_thread.start()
    interface_thread.start()
    ultrason_thread.start()
    