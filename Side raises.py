import cv2
import numpy as np
import streamlit as st
import PoseModule as pm

st.write("Steps to perform:")
st.write("Step 1: Stand with your feet shoulder-width apart, holding dumbbells at your sides.")
st.write("Step 2: Raise the weights out to the sides until they are level with your shoulders.")
st.write("Step 3: Lower the weights back to the starting position.")
st.write("Caution: People often tend to bend their neck forward along with putting pressure on teeth. ")
st.write("    Pls try to avoid that. Just smile, try to stand straight while performing this exercise.")

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

        anglL = detector.findAngle(img, 13, 11, 23)

        anglR = detector.findAngle(img, 14, 12, 24)
        percntL = np.interp(anglL, (19, 85), (0, 100))
        percntR = np.interp(anglR, (270, 330), (0, 100))

        if percntL == 100:
            if dirnL == 0:
                countL += 0.5
                dirnL = 1
        elif percntL == 0:
            if dirnL == 1:
                countL += 0.5
                dirnL = 0
        else:
            pass

        print(countL)
        cv2.rectangle(img, (0, frameHght - 50), (frameWid - 280, frameHght - 25), (193, 255, 8),
                      cv2.FILLED)
        cv2.putText(img, f'rep completion: {int(percntL)}%', (0, frameHght - 25), cv2.FONT_HERSHEY_PLAIN, 2,
                    (245, 42, 231), 2)
        if anglL > 88 and anglR < 265:
            cv2.putText(img, "raise exceed more than reqd", (0, 25), cv2.FONT_HERSHEY_PLAIN, 2,
                        (179, 3, 255), 2)
        elif (anglL > 18 and anglL < 87) and (anglR > 270 and anglR < 335):
            cv2.putText(img, "Good Going. Keep it up!!", (0, 25), cv2.FONT_HERSHEY_PLAIN, 2,
                        (0, 255, 0), 2)
        elif anglL > 88:
            cv2.putText(img, "excessive Left raise", (0, 25), cv2.FONT_HERSHEY_PLAIN, 2,
                        (179, 3, 255), 2)
        elif anglR < 265:
            cv2.putText(img, "excessive Right raise", (0, 25), cv2.FONT_HERSHEY_PLAIN, 2,
                        (179, 3, 255), 2)
        else:
            pass

    cv2.rectangle(img, (0, frameHght - 25), (frameWid - 280, frameHght), (8, 251, 255),
                  cv2.FILLED)
    cv2.putText(img, f'No. of reps: {int(countL)}', (0, frameHght), cv2.FONT_HERSHEY_PLAIN, 2, (8, 148, 255), 2)

    cv2.imshow("Vid", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()

