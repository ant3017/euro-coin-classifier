import numpy as np
import cv2
import time
from sys import argv


FRAME_WIDTH = 747

def collect_euro_coin(img):
    """Collect the euro coins from an image."""

    global OUTPUT_NAME

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Adaptive Thresholding
    gray_blur = cv2.GaussianBlur(gray, (15, 15), 0)
    thresh = cv2.adaptiveThreshold(gray_blur, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Circle detection
    circles = cv2.HoughCircles(gray_blur, cv2.HOUGH_GRADIENT, 1, 64,
                                param1=20, param2=40, minRadius=24,
                                maxRadius=96)

    if circles is not None:
        i = 0
        for c in circles[0]:
            name = (str(int((time.time() - 1400000000) * 1000))[-4:] + '-'
                + str(int(time.clock() * 100000000000))[-4:] + '-' + str(i))
            print 'Writing to "' + 'output/'+ name +'.jpg"'
            print c
            cv2.imwrite('output/'+ name +'.jpg',
                img[int(c[1]-c[2]):int(c[1]+c[2]),
                int(c[0]-c[2]):int(c[0]+c[2])])
            i += 1


if __name__ == "__main__":
    # If this script is running as a standalone program, start a demo
    if len(argv) > 1:
        for file_name in argv[1:]:
            print file_name
            img = cv2.imread(file_name)
            height, width, depth = img.shape
            roi = cv2.resize(img, (FRAME_WIDTH, FRAME_WIDTH * height / width))
            collect_euro_coin(roi)
        quit()
    option = raw_input('(V)ideo cam, or (L)oad an image file?')
    option = option.lower()
    if option == 'l':
        # Read from a file
        file_name = raw_input('Enter an image file name: ')

        img = cv2.imread(file_name)
        height, width, depth = img.shape
        roi = cv2.resize(img, (FRAME_WIDTH, FRAME_WIDTH * height / width))
        collect_euro_coin(img)


    elif option == 'v':
        # Start the video camera and show the detection results in real-time.
        cap = cv2.VideoCapture(0)

        while(True):
            ret, frame = cap.read()
            height, width, depth = frame.shape
            roi = cv2.resize(frame, (FRAME_WIDTH, FRAME_WIDTH * height / width))

            collect_euro_coin(roi)

            cv2.imshow('Video', roi)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
