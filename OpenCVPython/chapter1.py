import cv2
print("Package Imported")

## Picture access
# img = cv2.imread("data/greece.jpg")
# cv2.imshow("Output", img)
# cv2.waitKey(0)
#

## Video access
# cap = cv2.VideoCapture("data/screen_recording.mp4")
# while True:
#     success, test_image = cap.read()
#     cv2.imshow("Video", test_image)
#     if cv2.waitKey(1) & 0xFF ==ord('q'):
#         break

webcam_cap = cv2.VideoCapture(0)
webcam_cap.set(3, 640)
webcam_cap.set(4, 480)
webcam_cap.set(10, 100)

while True:
    success, test_image = webcam_cap.read()
    cv2.imshow("Webcam", test_image)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break

