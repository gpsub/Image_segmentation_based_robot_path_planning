from black import E
import pixellib
from pixellib.semantic import semantic_segmentation
import cv2
import numpy as np
from time import sleep;
import matplotlib.pyplot as plt
cap = cv2.VideoCapture()
cap.open("tcp://192.168.41.30:8888")
segment_video = semantic_segmentation()
segment_video.load_ade20k_model("deeplabv3_xception65_ade20k.h5")
# segment_video.process_camera_ade20k(cap, overlay=True, frames_per_second= 15, show_frames= True,
# frame_name= "Segmentation")


def get_mask(extracted_objects):
    mask = np.zeros(shape=(new_frame.shape[0],new_frame.shape[1]))
    color = [230,230,6]
    if mask.shape[0]>0 and mask.shape[1]>0:
        for i in range(new_frame.shape[0]):
            for j in range(new_frame.shape[1]):
                if((new_frame[i][j]==color).all()):
                    mask[i][j]=1
                else:
                    mask[i][j]=0

    mask = mask.astype(np.uint8)

    return mask

def findpath(mask):
   midpoints=[]
   for i in range(400,500):
        row_measure={"start":0,"end":0,"measure":0}
        measure=0
        max_measure=0 
        start=0
        for j in range(1,mask.shape[1]-1):
            if(measure==0):
                if(j<(mask.shape[1]-1) and mask[i][j]==1 and mask[i][j+1]==1):
                   measure+=1
                   start=j
            if(measure!=0):
                if(mask[i][j]==1 and mask[i][j+1]==1):
                    measure+=1
                    if(measure>max_measure and measure>40 and j>(mask.shape[1]-20)):
                            row_measure["start"]=start
                            row_measure["end"]=j
                            row_measure["measure"]=measure
                            max_measure=measure
                            measure=0;
                elif(measure>max_measure and measure>40):
                        row_measure["start"]=start
                        row_measure["end"]=j
                        row_measure["measure"]=measure
                        max_measure=measure
                        measure=0;
        midpoints.append(row_measure)
   x=[]
   y=[]
   for i in range(400,500):
        y.append(i);
        x.append((midpoints[i]["start"]+midpoints[i]["end"])//2)
   
   

while(True):
    _,frame = cap.read() # return a single frame in variable `frame`
    frame = cv2.flip(frame,0)
    segvalues, extracted_objects, new_frame= segment_video.segmentFrameAsAde20k(frame, output_frame_name="segmentation",overlay=True, verbose =False, extract_segmented_objects = True) 
    mask1 = get_mask(new_frame)
    # mask1 = mask1*255
    x,y = findpath(mask1)
    cv2.imshow("frames",new_frame) #display the captured image
    
    if cv2.waitKey(1) & 0xFF == ord('q'): #save on pressing 'y' 
        cv2.destroyAllWindows()
        break
cap.release()

