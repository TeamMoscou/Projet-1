import os
import threading
from rplidar import RPLidar

import time

import glob

from glob import *

from data import Data

from data import ID

from data import Message

from math import *

import numpy as np






Vitesse_V_y=5 #vitesse du vehicule suivant l'axe y en m/s

Vitesse_V_x=0 #vitesse du vehicule suivant l'axe x en m/s


#les coordonnées des points extremes de vehicule
Y0=1.0 ;# en m

X0=0.6;#en m

SAFE_DISTANCE = 3 ;#safety distance in m




# the definition of the class thread of the lidar
class LidarDetection(threading.Thread):


 def __init__(self,lidar):

        threading.Thread.__init__(self)

        self.lidar = lidar



 def run(self):

   print("Lidar thread begins")
   
   count_points_detected=0
   
   new_scan = True ;#true if lidar begins a new scan
   angle = 0.0 ;#retreive the angle of a scanned point in degrees
   quality = 0 ;#indicate the quality of the scan
   distance = 0.0 ;#retreive the distance a scanned point in mm 

   first_point_angle=None

   last_point_angle=None

   Obstacle_distance=0.0 ;#distance of the detected obstacle 

   Obstacle_angle=-1.0 ;#angle of the detected obstacle 

    

   refer_angle=-1.0 

   previous_liste_angles=[]

   previous_liste_distances=[]

   liste_angles=[]

   liste_distances=[]
   
   liste_tailles=[]

   delta_angles=[]

   delta_distances=[]

   liste_deltaTs=[]



   next_liste_angles=[]

   next_liste_distances=[]

   next_liste_deltaTs=[]

   next_liste_tailles=[] 

    

   prevT=[]
   next_prevT=[]

   currentT=0

   time.sleep(1)

   scan=[]

  
   for new_scan, quality,angle,distance in self.lidar.iter_measurments():

       if(not(new_scan) and distance!=0):
               
          scan.append((angle-180,distance/1000,quality))
          #time.sleep(.01)


       elif(new_scan) :
                                        
                scan=sorted(scan, key=lambda colonnes: colonnes[0])
                for i in range(len(scan)):
                
                        angle=scan[i][0] 
                        distance=scan[i][1]
                        
                        if (distance<=SAFE_DISTANCE and first_point_angle==None):

                            refer_angle=angle

                            first_point_angle=angle

                            last_point_angle=angle

                            count_points_detected=1

                            Obstacle_distance=distance

                        elif ( distance<=SAFE_DISTANCE and abs(angle-refer_angle)<= 3 ):

                            refer_angle=angle

                            last_point_angle=angle

                            count_points_detected=count_points_detected+1

                            Obstacle_distance=min(Obstacle_distance,distance)

                        elif (distance<=SAFE_DISTANCE and abs(angle-refer_angle)> 3) :#un nouveau obstacle

                            if(count_points_detected>5) : #je considère que c'est un obstacle

                                #Obstacle_distance=Obstacle_distance/count_points_detected

                                Obstacle_angle=(last_point_angle+first_point_angle)/2
                            

                                currentT=time.time()

                                if(liste_angles!=[]):

                                    delta_angles=[]
                                    delta_distances=[]

                                    for i in range(len(liste_angles)) :

                                        delta_angles.append(abs(liste_angles[i]-Obstacle_angle))

                                        delta_distances.append(abs(liste_distances[i]-Obstacle_distance))
                                   
                                    index=delta_angles.index(min(delta_angles))

                                    if(delta_angles[index]<=4 and delta_distances[index]<100):

                                        #liste_deltaTs[index]=currentT-prevT[index]

                                        next_liste_deltaTs.append(currentT-prevT[index])

                                        prevT[index]=currentT

                                        liste_angles[index]=Obstacle_angle

                                        liste_distances[index]=Obstacle_distance
                                        liste_tailles[index]=abs(2* Obstacle_distance*tan(radians((first_point_angle-last_point_angle)*0.5)))
                                        
                                    

                                    elif(delta_angles[index]>4):

                                        prevT.append(currentT)

                                        liste_angles.append(Obstacle_angle)

                                        liste_distances.append(Obstacle_distance)


                                        liste_tailles.append(abs(2*Obstacle_distance*tan(radians((first_point_angle-last_point_angle)*0.5))))

                                        #liste_deltaTs.append(-1)

                                        #next_liste_deltaTs.append(-1)

                                    

                                else :

                                    prevT.append(currentT)

                                    liste_angles.append(Obstacle_angle)

                                    liste_tailles.append(abs(2*Obstacle_distance*tan(radians((first_point_angle-last_point_angle)*0.5))))

                                    #liste_deltaTs.append(-1)


                                    #next_liste_deltaTs.append(-1)

                                    liste_distances.append(Obstacle_distance)

                                

                            

                                next_prevT.append(currentT)

                                next_liste_angles.append(Obstacle_angle)    

                                next_liste_distances.append(Obstacle_distance)

                                next_liste_tailles.append(abs(2*Obstacle_distance*tan(radians((first_point_angle-last_point_angle)*0.5))))
                    

                        

                            

                            

                                first_point_angle=angle

                                last_point_angle=angle

                                refer_angle=angle
  
                                count_points_detected=1

                                Obstacle_distance=distance

                            

                            else :

                                first_point_angle=angle

                                last_point_angle=angle

                                refer_angle=angle

                                count_points_detected=1

                                Obstacle_distance=distance

                        

                    

                            

                        elif(distance>SAFE_DISTANCE):

                            if(count_points_detected>5) : #je considère que c'est un obstacle

                                #Obstacle_distance=Obstacle_distance/count_points_detected

                                Obstacle_angle=(last_point_angle+first_point_angle)/2
                                
                                currentT=time.time()

                                if(liste_angles!=[]):

                                    delta_angles=[]
                                    delta_distances=[]

                                    for i in range(len(liste_angles)) :

                                        delta_angles.append(abs(liste_angles[i]-Obstacle_angle))

                                        delta_distances.append(abs(liste_distances[i]-Obstacle_distance))

                                    index=delta_angles.index(min(delta_angles))

                                    if(delta_angles[index]<=4 and delta_distances[index]<.1):

                                        #liste_deltaTs[index]=currentT-prevT[index]

                                        next_liste_deltaTs.append(currentT-prevT[index])

                                        prevT[index]=currentT

                                        liste_angles[index]=Obstacle_angle

                                        liste_distances[index]=Obstacle_distance


                                        liste_tailles[index]= abs(2*Obstacle_distance*tan(radians((first_point_angle-last_point_angle)*0.5)))

                                    elif(delta_angles[index]>4):

                                        prevT.append(currentT)

                                        liste_angles.append(Obstacle_angle)

                                        liste_distances.append(Obstacle_distance)

                                        liste_tailles.append(abs(2*Obstacle_distance*tan(radians((first_point_angle-last_point_angle)*0.5))))


                                        #liste_deltaTs.append(-1)

                                        #next_liste_deltaTs.append(-1)

                                    

                                else :

                                    prevT.append(currentT)

                                    liste_angles.append(Obstacle_angle)

                                    #liste_deltaTs.append(-1)

                                    #next_liste_deltaTs.append(-1)

                                    liste_distances.append(Obstacle_distance)

                                    liste_tailles.append(abs(2*Obstacle_distance*tan(radians((first_point_angle-last_point_angle)*0.5))))

                            
                                next_prevT.append(currentT)

                                next_liste_angles.append(Obstacle_angle)

                                next_liste_distances.append(Obstacle_distance)

                                next_liste_tailles.append(abs(2*Obstacle_distance*tan(radians((first_point_angle-last_point_angle)*0.5))))

                                #reinitiliser pour la prochaine iteration 

                                first_point_angle=None

                                last_point_angle=None

                                Obstacle_distance=0.0

                                Obstacle_angle=-1.0

                                count_points_detected=0

                            else: #qlq points detectes ( moins de 5 points ) jeter les
                            
                                #reinitiliser pour la prochaine iteration 

                                first_point_angle=None

                                last_point_angle=None

                                Obstacle_distance=0.0

                                Obstacle_angle=-1.0

                                count_points_detected=0

              
                first_point_angle=None

                last_point_angle=None

                Obstacle_distance=0.0

                Obstacle_angle=-1.0

                count_points_detected=0

                previous_liste_angles=liste_angles

                previous_liste_distances=liste_distances

                prevT=next_prevT

                liste_angles=next_liste_angles

                liste_distances=next_liste_distances

                liste_deltaTs=next_liste_deltaTs

                liste_tailles=next_liste_tailles



                
                sublist_forward_angles=[]
                sublist_forward_distances=[]
                sublist_forward_tailles=[]
                sublist_backward_angles=[]
                sublist_backward_distances=[]
                sublist_backward_tailles=[]
                
                for i in range(len(liste_angles)) :
                    if(abs(liste_angles[i])<90):
                        sublist_forward_angles.append(liste_angles[i])
                        sublist_forward_distances.append(liste_distances[i])
                        sublist_forward_tailles.append(liste_tailles[i])
                    else:
                        sublist_backward_angles.append(liste_angles[i])
                        sublist_backward_distances.append(liste_distances[i])
                        sublist_backward_tailles.append(liste_tailles[i])


                #print("FORWARD OBSTACLES")
                print ("front")
                print(sublist_forward_angles)
                print (sublist_forward_distances)
                print (sublist_forward_tailles)

                print("BACKWARD OBSTACLES")
                print(sublist_backward_angles)
                print (sublist_backward_distances)
                print (sublist_backward_tailles)
				
				
				
                TG_FRONT=0
                TD_FRONT=0
                action_FRONT="NO_DANGER"
                
                for i in range(len(sublist_forward_angles)) :

                    x=sublist_forward_distances[i]*sin(radians(sublist_forward_angles[i]))

                    #if(sublist_forward_distances[i]<2) :
                    #    action_FRONT="STOP"
                    #    break

                    
                    
                    if(abs(x)>(sublist_forward_tailles[i]+X0)/2.):
                    
                        """if(action_FRONT!="NO_DANGER"):
                            continue 
                        else:
			"""
                        action_FRONT="NO_DANGER"  
                        
                    elif (abs(x)<=(sublist_forward_tailles[i]+X0)/2.):

                        #situation ou l'obstacle est centre devant la voiture
                        if(abs(sublist_forward_angles[i])<5.): 
                            y=sublist_forward_distances[i]*tan(radians(10)) # 15° comme angle de deviation maximale des roues
                            """if(y>(sublist_forward_tailles[i]+X0)/2.):
                                TD_FRONT=1
                                if(TG_FRONT==1):
                                    action_FRONT="STOP"
                                    break
                                else:
                                    action_FRONT="TURN_RIGHT"
                                   
                            else:
                                #liste_action_FRONTs.append("STOP")
                            """
                            action_FRONT="STOP"
                            break
                        #il faut eviter obstacle a GAUCHE de la voiture
                        elif(x<0) :

                            TD_FRONT=1
                            if(TG_FRONT==1):
                                action_FRONT="STOP"
                                break
                            else:
                                action_FRONT="TURN_RIGHT"
                                print("hhhheeeeeereeeee")        
                        #il faut eviter obstacle a DROIT de la voiture
                        elif(x>0):
                            TG_FRONT=1
                            if(TD_FRONT==1):
                               action_FRONT="STOP"
                               break
                            else:
                               action_FRONT="TURN_LEFT"                                
                            
                       
                
                
                
                TG_BACK=0
                TD_BACK=0
                action_BACK="NO_DANGER"

                for i in range(len(sublist_backward_angles)) :

                    x=sublist_backward_distances[i]*sin(radians(sublist_backward_angles[i]))
                    
                    if(abs(x)>(sublist_backward_tailles[i]+X0)/2.):
                    
                        if(action_BACK!="NO_DANGER"):
                            continue 
                        else:
                            action_BACK="NO_DANGER"  
                        
                    elif (abs(x)<=(sublist_backward_tailles[i]+X0)/2.):

                        #situation ou l'obstacle est centre devant la voiture
                        if(abs(sublist_backward_angles[i])<7.): 
                            y=sublist_backward_distances[i]*tan(radians(10)) # 15° comme angle de deviation maximale des roues
                            print("y=",y)
                            print( "a=",b)
                            if(y>(sublist_backward_tailles[i]+X0)/2.):
                                """TD_BACK=1
                                if(TG_BACK==1):
                                    action_BACK="STOP"
                                    break
                                else:
                                    action_BACK="TURN_RIGHT"
                                """   
                                #else:
                                #liste_action_BACKs.append("STOP")
                                action_BACK="STOP"
                                break
                                
                        #il faut eviter obstacle a DROIT de la voiture
                        elif(x>0):
                            TG_BACK=1
                            if(TD_BACK==1):
                               action_BACK="STOP"
                               break
                            else:
                               action_BACK="TURN_LEFT"                                 
                            
                        #il faut eviter obstacle a GAUCHE de la voiture
                        else :

                            TD_BACK=1
                            if(TG_BACK==1):
                                action_BACK="STOP"
                                break
                            else:
                                action_BACK="TURN_RIGHT"
                                
                                
                
                              
                print ("Action Front",action_FRONT)
                
                print ("Action BACK",action_BACK)


                if(action_FRONT=="NO_DANGER") :
                        glob.DATA_LIDAR_AUTONOMOUS.message = Message.FORWARD
                elif(action_FRONT=="STOP"):
                        glob.DATA_LIDAR_AUTONOMOUS.message = Message.STOP
                elif(action_FRONT=="TURN_LEFT"):
                        glob.DATA_LIDAR_AUTONOMOUS.message = Message.FORWARD_LEFT
                else:
                        glob.DATA_LIDAR_AUTONOMOUS.message = Message.FORWARD_RIGHT
                print("in lidar DATA AUTO "+ str(glob.DATA_LIDAR_AUTONOMOUS.message))
                
                if(action_BACK=="NO_DANGER" and action_FRONT=="NO_DANGER"):
                    glob.DATA_LIDAR.message=Message.DETECTED_NULL
                elif(action_BACK!="NO_DANGER" and action_FRONT=="NO_DANGER"):
                    glob.DATA_LIDAR.message=Message.DETECTED_BACK
                elif(action_BACK=="NO_DANGER" and action_FRONT!="NO_DANGER"):
                    glob.DATA_LIDAR.message=Message.DETECTED_FRONT
                else:
                    glob.DATA_LIDAR.message=Message.DETECTED_BOTH
                    
                    




                next_liste_angles=[]

                next_liste_deltaTs=[]

                next_liste_distances=[]

                next_liste_tailles=[]

                next_prevT=[]
                  
                scan=[]




