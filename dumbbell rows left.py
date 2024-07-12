import cv2
import numpy as np
import PoseModule as pm
import streamlit as st

st.write("Steps to perform:")
st.write("Step 1: Place right knee and right hand on a bench, holding a dumbbell in the left hand. ")
st.write("Step 2: The upper body should be parallel to floor and spine should not be bent forward. ")
st.write("        Prefer a mirror in front to look your face exactly in this position. ")
st.write("        Other feet should be placed a little backwards. ")
st.write("Step 3: Lower the dumbbell in your left hand to the lowest position such that the left shoulder is slightly"
         "    declined with respect to right shoulder")
st.write("Step 4: Slowly pull the dumbbell towards the hip in such a way that finally the angle between bicep and "
         "   forearm is near about 90 deg. (Note: Target is not to make the dumbbell reach the hip as final position)")
st.write("      Important thing is that peak contraction should be felt at lat muscle. ")
st.write("Step 5: Slowly lower the dumbbell back to the starting position.")

cap = cv2.VideoCapture(0)
frameWid = int((cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
frameHght = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
cap.set(3, frameWid)
cap.set(4, frameHght)
cap.set(10, 150)

detector = pm.poseDetector()

countL = 0
countR = 0
dirnL = 0
dirnR = 0

while True:
    success, img = cap.read()
    img = detector.findPose(img, False)
    lmlist = detector.findPosition(img, False)

    if len(lmlist) != 0:

        anglL = detector.findAngle(img, 11, 13, 15)
        percntL = np.interp(anglL, (187, 277), (0, 100))

        if percntL == 100:
            if dirnL == 0:
                countL += 0.5
                dirnL = 1
        if percntL == 0:
            if dirnL == 1:
                countL += 0.5
                dirnL = 0
        print(countL)
        if anglL > 277:
            cv2.putText(img, "pulled more than reqd", (0, 25), cv2.FONT_HERSHEY_PLAIN, 2,
                        (0, 0, 255), 2)
        cv2.rectangle(img, (0, frameHght - 50), (frameWid - 280, frameHght - 25), (193, 255, 8),
                      cv2.FILLED)
        cv2.putText(img, f'rep completion: {int(percntL)}%', (0, frameHght - 25), cv2.FONT_HERSHEY_PLAIN, 2,
                    (245, 42, 231), 2)

    cv2.rectangle(img, (0, frameHght - 25), (frameWid - 280, frameHght), (8, 251, 255),
                  cv2.FILLED)
    cv2.putText(img, f'No. of reps: {int(countL)}', (0, frameHght), cv2.FONT_HERSHEY_PLAIN, 2, (8, 148, 255), 2)

    cv2.imshow("Vid", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()

