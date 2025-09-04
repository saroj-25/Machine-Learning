import cv2
import numpy as np
import os
import time

color_bgr={
 "Red":(0,0,255),
 "Blue":(255,0,0),
 "Green":(0,255,0),
 "Yellow":(0,255,255),
 "Black":(0,0,0)
}

class ColorTracker:
 def __init__(self):
    self.colors=[
     ("Red",[0,120,70],[10,255,255]),
     ("Blue",[90,150,0],[140,255,255]),
     ("Green",[40,70,70],[80,255,255]),
     ("Yellow",[20,100,100],[30,255,255]),
     ("Black",[0,0,0],[180,255,30])
    ]
    self.model_dir="captures"
    if not os.path.exists(self.model_dir):
        os.makedirs(self.model_dir)

 def track(self,frame):
    centers=[]
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    detected_color="unknown"
    max_area=0
    for name,low,high in self.colors:
        low=np.array(low)
        high=np.array(high)
        if name=="Red":
            mask1=cv2.inRange(hsv,np.array([0,120,70]),np.array([10,255,255]))
            mask2=cv2.inRange(hsv,np.array([170,120,70]),np.array([180,255,255]))
            mask=mask1+mask2
        else:
            mask=cv2.inRange(hsv,low,high)
        cnts,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for c in cnts:
            area=cv2.contourArea(c)
            if area>500:
                x,y,w,h=cv2.boundingRect(c)
                cv2.rectangle(frame,(x,y),(x+w,y+h),color_bgr[name],2)
                text_color=(255,255,255) if name=="Black" else color_bgr[name]
                cv2.putText(frame,name,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.6,text_color,2)
                centers.append((x+w//2,y+h//2))
                if area>max_area:
                    max_area=area
                    detected_color=name
    return frame,centers,detected_color

 def save_frame(self,frame,color_name):
    timestamp=int(time.time())
    filename=os.path.join(self.model_dir,f"{color_name}_{timestamp}.jpg")
    cv2.imwrite(filename,frame)
    print(f"Saved {filename}")
