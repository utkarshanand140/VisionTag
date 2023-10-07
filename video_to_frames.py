import cv2

vid_capture = cv2.VideoCapture('Drone-Videos/7.mp4') # Path of the video to be broken into frames
if (vid_capture.isOpened() == False):
    print("Error opening video file")
else:
    i = -1
    while(vid_capture.isOpened()):
        i = i+1
        ret, frame = vid_capture.read()
        if ret == True:
            path = f"Images/frame{i}.png"
            cv2.imwrite(path,frame)
            print(path)
        else:
            print("Process Completed!")
            break

    vid_capture.release()
