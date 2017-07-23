# Required moduls
import cv2                                           #OpenCV library supports a lot of algorithms related to Computer Vision and Machine Learning.
import object                                        #Numpy is a highly optimized library for numerical operations.
import serial                                        #Serial module encapsulates the access for the serial port.
import math                                          #Math module provides access to the mathematical functions defined by the C standard.
import time                                          #Time module provides various time-related functions.


                                     
ser=serial.Serial('/dev/ttyACM0')                    #opens a serial port with 9600 Baud rate
min_area = 8000                                      #setting minimum value for skin detected area                                       
numbered = []                                        #list to store sorted points of approximated polygon obtained from cv2.approxPolyDP
data=[]                                              #list to store data recieved from arduino(to check whether it has recieved same data as that of we are sending)

#Constants for finding range of skin color in YCrCb
min_YCrCb = numpy.array([120,120,110],numpy.uint8)   #storing minimum contents of RGB in skin color 
max_YCrCb = numpy.array([252,230,220],numpy.uint8)   #storing maximum contents of RGB in skin color

font = cv2.cv.InitFont(cv2.FONT_HERSHEY_COMPLEX, 1, 1, 0, 3, 5) #Creates a font

cv2.namedWindow('Camera Output')                     #Creates a window to display the camera feed

videoFrame = cv2.VideoCapture(1)                     #Get pointer to video frames from primary device

# Process the video frames
while (1):
    prev_x = 0

    readSucsess, sourceImage = videoFrame.read()                                        #Grab video frame, decode it and return next video frame
    
    imageYCrCb = cv2.cvtColor(sourceImage,cv2.COLOR_BGR2YCR_CB)                         #Convert image to YCrCb

    skinRegion = cv2.inRange(imageYCrCb,min_YCrCb,max_YCrCb)                            #Find region with skin tone in YCrCb image

    #The function retrieves contours from the binary image using the Suzuki algorithm .
    #The contours are a useful tool for shape analysis and object detection and recognition
    contours, hierarchy = cv2.findContours(skinRegion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #finding contours on skin region

    for i, c in enumerate(contours):                                            #looping through all the contours obtained from previous step
        area = cv2.contourArea(c)                                               #Calculates a contour area & stores it in area
        if area > min_area:                                                     #checking whether contour is greater than 'min_area',if yes:
            ci = i                                                              #store the index of that contour in 'ci'
            cv2.drawContours(sourceImage, contours, i, (0, 255, 0), 3)          #Draws contours outlines on 'sourceImage'
            
    cnt=contours[ci]                                                            #getting a contour which is human hand
    
    hull = cv2.convexHull(cnt)                                                  #The functions find the convex hull of a 2D point set using the Sklansky’s algorithm 
    moments = cv2.moments(cnt)                                                  #Calculates all of the moments up to the third order of a polygon or rasterized shape

    if moments['m00']!=0:                                                       #computes the center of the contour
                cx = int(moments['m10']/moments['m00'])                         # cx = M10/M00   x-cordinate of center of contour       
                cy = int(moments['m01']/moments['m00'])                         # cy = M01/M00   y-cordinate of center of contour
                
    centr=(cx,cy)                                                               #storing center of contour
    cv2.drawContours(sourceImage,[hull],0,(0,0,255),2)                          #Draws contours outlines on 'sourceImage' using hull
          
    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)    #Approximates a polygonal curve(s) with the specified precision using Douglas-Peucker algorithm
    l = list(approx)                                                    #converting array into lists
    
    hull = cv2.convexHull(cnt,returnPoints = False)                     #it returns indices of the convex hull points     
    if(1):
            
               defects = cv2.convexityDefects(cnt,hull)    #finds all convexity defects of the input contour and returns a sequence of the CvConvexityDefect structures
               mind=0
               maxd=0
               for i in range(defects.shape[0]):
                    s,e,f,d = defects[i,0]
                    start = tuple(cnt[s][0])                      #point of the contour where the defect begins
                    end = tuple(cnt[e][0])                        #point of the contour where the defect ends
                    far = tuple(cnt[f][0])                        #the farthest from the convex hull point within the defect
                    dist = cv2.pointPolygonTest(cnt,centr,True)   #The function determines whether the point is inside a contour, outside, or lies on an edge.
                    cv2.line(sourceImage,start,end,[0,255,0],2)   #The function line draws the line segment between pt1 and pt2 points in the image. 
                    cv2.circle(sourceImage,far,5,[0,0,255],-1)    #The function 'circle' draws a simple or filled circle with a given center and radius.
               i=0
               
    for i,item in (enumerate(l)):                                 #looping through list 'l'
        item.tolist()                                             #converting each item of 'l' to list to perform operations(as they are in 'ndarray' form)
        if ((item[0][0] >= 400) & (item[0][1] < 400)):            #getting a point which has highest width in an image
            if item[0][0] > prev_x:                               #checking whether current point has greater width than prev_x,if yes:
                prev_x = item[0][0]                               #store this value in 'prev_x'
                index = i                                         #store the index of that point in 'index' variable
                
    numbered.extend(l[index:])                                    #extend 'numbered' list with list 'l'(which is sliced from index 'index' to the last index)
    if index!=0:                                                  #if index is not equal to zero then:
        numbered.extend(l[:index])                                #extend 'numbered' list with list 'l'(which is sliced from index 0 to the index 'index')
        
    for i,item in (enumerate(numbered)):                          #for every item in 'numbered' do following operations:
        item.tolist()                                             #convert each item to list
        cv2.circle(sourceImage,(item[0][0],item[0][1]),5,[0,0,255],2)         #The function 'circle' draws a simple or filled circle with a given center and radius.
        img=cv2.cv.fromarray(sourceImage)                                     #converting numpy array to opencv array
        cv2.cv.PutText(img, str(i), (item[0][0],item[0][1]),font, (255,0,0))  #The function 'putText' renders the specified text string in the image
        
    #determining shoulder,elbow,wrist & gripper points       
    for i,item in enumerate(numbered):                           #looping through 'numbered' list
        item.tolist()                                            #convert each item to list
        if(i==1):                                                #shoulder joint                                 
            x1=item[0][0]
            y1=item[0][1]
        if(i==2):                                                #elbow joint
            x2=item[0][0]
            y2=item[0][1]
        if(i==3):                                                #first wrist point
            x3=item[0][0]
            y3=item[0][1]
        if(i==4):                                                #second wrist point                                
            x4=item[0][0]
            y4=item[0][1]
        if(i==6):                                                #first gripper point                                       
            x6=item[0][0]
            y6=item[0][1]
        if(i==8):                                                #second gripper point
            x8=item[0][0]
            y8=item[0][1]
        
    #Calculates angle between elbow & shoulder and sends it serially
    if(abs(x2-x1)>0):                                                                #condition to avoid 'divide by zero' error
        angle_elbow_shoulder=int(math.atan2((y2-y1),(x1-x2))*180/math.pi)            #calculating angle between elbow & shoulder       
        if(angle_elbow_shoulder >= 0):                                               #if 'angle_elbow_shoulder' is positive,then:
            if(angle_elbow_shoulder < 45):                                           #check whether 'angle_elbow_shoulder' is less than 45 degress,if yes:
                s=45-angle_elbow_shoulder                                            #subtract it from 45 to obtain proper angle to be given to servo motor
            else:                                                                    #if it is greater than 45, send 0 degrees to the servo
                s=0
            ser.write(str('S'+str(s)+'\n'))                                          #it sends string of ('S'+str(s)+'\n') to the arduino serially,
                                                                                     #'S' is to indicate shoulder,'s' is the angle &'\n' to indicate end of the data 
            time.sleep(0.6)                                                          #delay of 0.6sec for servo to react properly before the next data is ready to send                                               
                
            while(ser.inWaiting()>0):                                                #serially receiving data back from arduino
                if(ser.read()!='\n'):                                                #read data till '\n'
                    data.append(ser.read())                                          #append the recieved data to list 'data'
                print data                                                           #print list 'data'

    #Calculates angle between elbow & wrist and sends it serially        
    if(abs(x2-x3)>0):                                                                #condition to avoid 'divide by zero' error
        angle_elbow_wrist=int(math.atan2((y2-y3),(x3-x2))*180/math.pi)               #calculating angle between elbow & wrist
        if(angle_elbow_wrist <0):                                                    #if 'angle_elbow_wrist' is negative,then:
            x=-angle_elbow_wrist-135                                                 #obtain proper angle to be given to servo motor      
            ser.write(str('E'+str(x)+'\n'))                                          #it sends string of ('E'+str(x)+'\n') to the arduino serially,
                                                                                     #'E' is to indicate Elbow,'x' is the angle &'\n' to indicate end of the data  
            time.sleep(0.6)                                                          #delay of 0.6sec for servo to react properly before the next data is ready to send 
            
            while(ser.inWaiting()>0):                                                #serially receiving data back from arduino
                if(ser.read()!='\n'):                                                #read data till '\n'
                    data.append(ser.read())                                          #append the recieved data to list 'data'
                print data                                                           #print list 'data'
                
        elif(angle_elbow_wrist > 0):                                                 #if 'angle_elbow_wrist' is positive,then:
            y=225-angle_elbow_wrist                                                  #obtain proper angle to be given to servo motor  
            ser.write(str('E'+str(y)+'\n'))                                          #it sends string of ('E'+str(x)+'\n') to the arduino serially,
                                                                                     #'E' is to indicate Elbow,'y' is the angle &'\n' to indicate end of the data
            time.sleep(0.6)                                                          #delay of 0.6sec for servo to react properly before the next data is ready to send
            while(ser.inWaiting()>0):                                                #serially receiving data back from arduino
                if(ser.read()!='\n'):                                                #read data till '\n'
                    data.append(ser.read())                                          #append the recieved data to list 'data'
                print data                                                           #print list 'data'

    #Calculates angle between 2 wrist points and sends it serially
    #explanation is same as above
    if(abs(x4-x3)>0):
        angle_wrist=int(math.atan2((y3-y4),(x4-x3))*180/math.pi)
        if(angle_wrist <0):
                
            z=-136-angle_wrist
            ser.write(str('W'+str(z)+'\n'))
            time.sleep(0.6)
            while(ser.inWaiting()>0):
                if(ser.read()!='\n'):
                    data.append(ser.read())
                print data
        elif(angle_wrist > 0):
            k=225-angle_wrist
            ser.write(str('W'+str(k)+'\n'))
            time.sleep(0.6)
            while(ser.inWaiting()>0):
                if(ser.read()!='\n'):
                    data.append(ser.read())
                print data

    dist = math.pow((math.pow((x6-x8),2)+math.pow((y6-y8),2)),0.5)  #calculates distance between 2 gripper points using distance formula
    di = int(dist/3)                                                #converting distance to an angle by dividing it by proper scalar(in this case,it is 3)
    ser.write(str('G'+str(di)+'\n'))                                #it sends string of ('G'+str(di)+'\n') to the arduino serially,
                                                                    #'G' is to indicate Gripper,'di' is the angle &'\n' to indicate end of the data
    time.sleep(0.6)                                                 #delay of 0.6sec for servo to react properly before the next data is ready to send
                         
    cv2.imshow('Camera Output',sourceImage)                         #show the 'sourceImage' in 'Camera Output' window
    numbered = []                                                   #empty the list 'numbered'
    data = []                                                       #empty the list 'data'

    k = cv2.waitKey(10)                                             #wait for the user to press key
    if k == 27:                                                     #if user pressed 'escape' key
        break                                                       #then break out of while loop

cv2.destroyWindow('Camera Output')                                  #destroy the window
videoFrame.release()                                                #release the video frame



