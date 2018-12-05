from threading import Thread
import threading



class Data:
    Message=""

def prise_decision(DataLidar,DataUltrason,DataInterface,DataOut):
    global Mode
    if (Mode=="Pilote" or Mode=="Autonomous"):
    
        if (DataInterface.Message == "STOP" or DataLidar.Message == "STOP" or DataUltrason.Message == "STOP"):
            DataOut.Message="STOP"
      
            if (Mode=="Pilote"):
                
                Mode="Autonomous"
             
        else:
            DataOut.Message=DataInterface.Message

''' Partie test
Test_Lidar = Data()
Test_Ultrason = Data()
Test_Interface = Data()
Test_Out = Data()
Test_Lidar.Message="STOP"
Test_Ultrason.Message="mi"
Test_Interface.Message="m"
Mode="Autonomous"
prise_decision(Test_Lidar,Test_Ultrason,Test_Interface,Test_Out)
print(Test_Out.Message)
print(Mode)
    
'''
