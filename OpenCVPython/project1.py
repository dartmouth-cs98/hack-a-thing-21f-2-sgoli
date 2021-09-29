import cv2
import numpy as np
# get webcam
frameWidth = 640
frameHeight = 480
webcam_cap = cv2.VideoCapture(0)
webcam_cap.set(3, frameWidth)
webcam_cap.set(4, frameHeight)
webcam_cap.set(10, 130)

def preProcessing(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, 200, 200)
    kernel = np.ones((5, 5))
    imgDial = cv2.dilate(imgCanny, kernel, 2)
    imgThres = cv2.erode(imgDial, kernel, 1)

    return imgThres

def getContours(img):
    biggestArea = np.array([])
    maximumArea = 0
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        # print(area)
        if area > 500:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            perimeter = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*perimeter, True)
            if area > maximumArea and len(approx) == 4:
                print('here')
                biggestArea = approx
                maximumArea = area

    return biggestArea

def reorder(myPoints):
    myPoints = myPoints.reshape((4,2))
    myPointsNew = np.zeroes((4,1,2), np.int32)
    add = myPoints.sum(1)

    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]

    return myPointsNew

def getWarp(img, biggest):
    new_biggest = reorder(biggest)
    pts1 = np.float32(new_biggest)
    pts2 = np.float32([[0, 0], [frameWidth, 0], [0, frameHeight], [frameWidth, frameHeight]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv2.warpPerspective(img, matrix, (frameWidth, frameHeight))

    imgCropped = imgOutput[20:imgOutput.shape[0]-20, 20:imgOutput.shape[1]-20]
    imgCropped = cv2.resize(imgCropped, (frameWidth, frameHeight))

    return imgCropped

while True:
    success, img = webcam_cap.read()
    cv2.resize(img, (frameWidth, frameHeight))
    imgContour = img.copy()

    imgThreshold = preProcessing(imgContour)
    biggest = getContours(imgThreshold)
    print(biggest)
    # warpedImage = getWarp(img, biggest)

    cv2.imshow("Webcam", imgContour)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break
