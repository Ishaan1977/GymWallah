import cv2
import numpy as np
import streamlit as st
import PoseModule as pm

st.write("Steps to perform:")
st.write("Step 1: Place left knee and left hand on a bench, holding a dumbbell in the right hand. ")
st.write("Step 2: The upper body should be parallel to floor and spine should not be bent forward. ")
st.write("        Prefer a mirror in front to look your face exactly in this position. ")
st.write("        Other feet should be placed a little backwards. ")
st.write("Step 3: Lower the dumbbell in your right hand to the lowest position such that the right shoulder is slightly"
         "    declined with respect to left shoulder")
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

        anglR = detector.findAngle(img, 12, 14, 16)
        percntR = np.interp(anglR, (170, 103), (0, 100))

        if percntR == 100:
            if dirnR == 0:
                countR += 0.5
                dirnR = 1
        if percntR == 0:
            if dirnR == 1:
                countR += 0.5
                dirnR = 0
        print(countR)
        if anglR < 103:
            cv2.putText(img, "pulled more than reqd", (0, 25), cv2.FONT_HERSHEY_PLAIN, 2,
                        (0, 0, 255), 2)
        cv2.rectangle(img, (0, frameHght - 50), (frameWid - 280, frameHght - 25), (193, 255, 8),
                      cv2.FILLED)
        cv2.putText(img, f'rep completion: {int(percntR)}%', (0, frameHght - 25), cv2.FONT_HERSHEY_PLAIN, 2,
                    (245, 42, 231), 2)

    cv2.rectangle(img, (0, frameHght - 25), (frameWid - 280, frameHght), (8, 251, 255),
                  cv2.FILLED)
    cv2.putText(img, f'No. of reps: {int(countR)}', (0, frameHght), cv2.FONT_HERSHEY_PLAIN, 2, (8, 148, 255), 2)

    cv2.imshow("Vid", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()

