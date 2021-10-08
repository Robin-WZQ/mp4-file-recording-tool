"""
    @function: read from USB camera
    @author: Robin_WZQ
    @date: 2021/10/8
    @software: VSCode
"""
import datetime
import os

import cv2


def read_usb_capture():
    # choose the number of the camera
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('real_img', cv2.WINDOW_NORMAL)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('temp.mp4', fourcc, 25, (640, 480))
    i=0
    while(cap.isOpened()):
        i+=1
        # read the camera
        ret, frame = cap.read()

        # write the video
        out.write(frame)
        # real picture
        cv2.imshow('real_img', frame)
        # press 'esc' to exit
        if cv2.waitKey(1) & 0xFF == 27:
            break
    # release the picture
    cap.release()
    cv2.destroyAllWindows()

def main():
    os.system("start cmd_.vbe") #start to recording audio
    read_usb_capture() #start to recoding video
    name = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  # current time
    os.system("ffmpeg -i temp.mp4 -i temp.wav -strict -2 -f mp4 " +"data/"+ name + ".mp4")  # use ffmpeg to combine
    os.remove('temp.mp4') 
    os.remove("temp.wav") 

if __name__=="__main__":
    name = main()
