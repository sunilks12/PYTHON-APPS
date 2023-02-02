import cv2
import time
import glob
import os
from threading import Thread
from emailing import send_email

video=cv2.VideoCapture(0)
time.sleep(1)
first_frame=None
status_list=[]
count=1



def clean_folder():
    images=glob.glob('images/*.png')
    for image in images:
    	os.remove(image)


while True:

    status=0 # to capture the static and movment later in rectangle ,capture after new object exits the frame
    check, frame=video.read()
  
    gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray_frame_gau=cv2.GaussianBlur(gray_frame,(21,21),0) # to reduce the noise
    
    # each frame will be compared to first frame in order to detect the movement
    if first_frame is None:
        first_frame=gray_frame_gau
        
    delta_frame=cv2.absdiff(first_frame,gray_frame_gau)
 
    
    thresh_frame=cv2.threshold(delta_frame,60, 255,cv2.THRESH_BINARY)[1] # 255 is white and we are considering pixel value >60 and assign it to 255
    dil_frame=cv2.dilate(thresh_frame, None, iterations=2) # deletes the noise and then we have to create the contours
    cv2.imshow("My video",thresh_frame)
    
    contours, check = cv2.findContours(dil_frame,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) # TO DETECT THE NEW OBJECT
    
    for contour in contours:
        if cv2.contourArea(contour)<5000: # to check fake object
            continue
        x,y,w,h = cv2.boundingRect(contour)
        rectangle=cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
        if rectangle.any():
            status=1
            cv2.imwrite(f"images/{count}.png",frame)
            count=count+1
            all_images=glob.glob("images/*.png")
            index=int(len(all_images)/2)
            image_with_object=all_images[index]
           
    status_list.append(status)   
    status_list=status_list[-2:] # get only the last two objects of the array
    
    if status_list[0]==1 and status_list[1]==0: # just exited the frame 
        email_thread=Thread(target=send_email,args=(image_with_object, ))
        #send_email(image_with_object) we dont need this since using thread
        email_thread.daemon=True
        clean_thread=Thread(target=clean_folder)
        #send_email(image_with_object) we dont need this since using thread
        clean_thread.daemon=True
        #clean_folder()
        
        email_thread.start()
      
    

    cv2.imshow("video",frame)
    key=cv2.waitKey(1)
    
    if key==ord("q"):
        break
video.release()  
clean_thread.start()