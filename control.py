import cv2
from time import*
import hand as htm
from math import*
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np

pTime = 0
cap = cv2.VideoCapture(0)
detector = htm.handDetector(detectionCon=0.8)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
mixVol = volRange[0]
maxVol = volRange[1]



while True:
    ret, frame = cap.read()
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame,draw=False)

    
    if len(lmList)!=0:
        print(lmList[4],lmList[8])
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        cv2.circle(frame,(x1,y1),15,(255,255,0),-1)
        cv2.circle(frame,(x2,y2),15,(255,255,0),-1)
        cv2.line(frame,(x1,y1),(x2,y2),(255,255,0),5)

        cv2.circle(frame,((x1+x2)//2,(y1+y2)//2),15,(255,255,0),-1)

        length_of_line = hypot(x2-x1,y2-y1)
        # print(length_of_line)
        # 20-300
        vol = np.interp(length_of_line,[25,300],[mixVol,maxVol])
        vol_for_rectengle = np.interp(length_of_line,[25,300],[400,150])
        percentage = np.interp(length_of_line,[25,300],[0,100])
        volume.SetMasterVolumeLevel(vol, None)
        if length_of_line < 20:
            cv2.circle(frame,((x1+x2)//2,(y1+y2)//2),15,(0,255,0),-1)

        cv2.rectangle(frame,(50,150),(100,400),(0,255,0), 3)
        cv2.rectangle(frame,(50,int(vol_for_rectengle)),(100,400),(0,255,0), -1)

        font = cv2.FONT_ITALIC
        cv2.putText(frame, f"Volume: {int(percentage)}%",(10,140),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),3)

    cTime= time()
    cTime= time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(frame, f"FPS: {int(fps)}",(150,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

    


    cv2.imshow("NPD5.0", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()