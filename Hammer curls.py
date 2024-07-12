import cv2
import numpy as np
import PoseModule as pm
import streamlit as st

st.write("Step 1: Stand with your feet shoulder-width apart, holding dumbbells with a neutral grip.")
st.write("Step 2: Curl the weights towards your shoulders just like you are lifting a mini hammer to penetrate a nail")
st.write("        in horizontally kept flat wooden piece .")
st.write("Step 3: Lower the weights back to the starting position.")
st.write()
st.write()

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

        anglR = detector.findAngle(img, 12, 14, 16)
        percntL = np.interp(anglL, (12, 150), (0, 100))
        percntR = np.interp(anglR, (184, 344), (0, 100))

        if percntL == 100:
            if dirnL == 0:
                countL += 0.5
                dirnL = 1
        if percntL == 0:
            if dirnL == 1:
                countL += 0.5
                dirnL = 0
        if percntR == 100:
            if dirnR == 0:
                countR += 0.5
                dirnR = 1
        if percntR == 0:
            if dirnR == 1:
                countR += 0.5
                dirnR = 0

        print(f'countL {countL}')
        print(f'countL {countR}')
        if (anglL > 12 and anglL < 180) or (anglR > 182 and anglR < 346):
            cv2.putText(img, "Very well. Keep doing", (0, 25), cv2.FONT_HERSHEY_PLAIN, 2,
                        (0, 255, 0), 2)
        cv2.rectangle(img, (0, frameHght - 75), (frameWid - 250, frameHght - 50), (193, 255, 8),
                      cv2.FILLED)
        cv2.putText(img, f'rep completion(R):{int(percntR)}%', (0, frameHght - 50), cv2.FONT_HERSHEY_PLAIN, 2,
                    (245, 42, 231), 2)
        cv2.rectangle(img, (0, frameHght - 100), (frameWid - 250, frameHght - 75), (94, 252, 3),
                      cv2.FILLED)
        cv2.putText(img, f'rep completion(L):{int(percntL)}%', (0, frameHght - 75), cv2.FONT_HERSHEY_PLAIN, 2,
                    (245, 42, 231), 2)

    cv2.rectangle(img, (0, frameHght - 50), (frameWid - 250, frameHght - 25), (8, 251, 255),
                  cv2.FILLED)
    cv2.putText(img, f'No. of reps(L): {int(countL)}', (0, frameHght - 25), cv2.FONT_HERSHEY_PLAIN, 2, (8, 148, 255), 2)

    cv2.rectangle(img, (0, frameHght - 25), (frameWid - 250, frameHght), (8, 148, 255),
                  cv2.FILLED)
    cv2.putText(img, f'No. of reps(R): {int(countR)}', (0, frameHght), cv2.FONT_HERSHEY_PLAIN, 2, (8, 251, 255), 2)

    cv2.imshow("Vid", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()

