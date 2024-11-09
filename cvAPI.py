import cv2
import numpy as np
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time

class VisionClient:

    def __init__(self, classes):
        self.ap = argparse.ArgumentParser()
        self.ap.add_argument("-p", "--prototxt",
                             required=True, help="SSD_MobileNet_prototxt.txt")
        self.ap.add_argument("-m", "--model",
                             required=True, help="SSD_MobileNet.caffemodel")
        self.ap.add_argument("-c", "--confidence", type=float, default=0.2,
	                        help="minimum probability to filter weak detections")
        self.args = vars(self.ap.parse_args())
        self.classes = classes
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))
        self.net = cv2.dnn.readNetFromCaffe(self.args["prototxt"], self.args["model"])

    def video_CV(self, file='', stream=False):
        if stream == False:
            video = VideoStream(src=file).start()
            fps = FPS.start(0)
        else:
            video = VideoStream(src=0).start()
            time.sleep(2.0)
            fps = FPS.start(0)
        
        item_track = {}

        playback = True
        while playback == True:
            # grab the frame from the threaded video stream and resize it
            # to have a maximum width of 400 pixels
            frame = video.read()
            frame = imutils.resize(frame, width=400)
            # grab the frame dimensions and convert it to a blob
            (h, w) = frame.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
                0.007843, (300, 300), 127.5)
            # pass the blob through the network and obtain the detections and
            # predictions
            self.net.setInput(blob)
            detections = self.net.forward()

            # loop over the detections
            for i in np.arange(0, detections.shape[2]):
                # extract the confidence (i.e., probability) associated with
                # the prediction
                confidence = detections[0, 0, i, 2]
                # filter out weak detections by ensuring the `confidence` is
                # greater than the minimum confidence
                if confidence > self.args["confidence"]:
                    # extract the index of the class label from the
                    # `detections`, then compute the (x, y)-coordinates of
                    # the bounding box for the object
                    idx = int(detections[0, 0, i, 1])
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    # draw the prediction on the frame
                    label = "{}: {:.2f}%".format(self.classes[idx],
                        confidence * 100)
                    item_track[label] = [frame, startX, startY]
                    y = startY - 15 if startY - 15 > 15 else startY + 15
                
                key = cv2.waitKey(1) & 0xFF
                # if the `q` key was pressed, break from the loop
                if key == ord("q"):
                    break
                # update the FPS counter
                fps.update()

            # stop the timer and display FPS information
            fps.stop()
            # do a bit of cleanup
            cv2.destroyAllWindows()
            video.stop()
            playback = False
            return item_track

#todo: break loop after video ends
#whole thing is completely screwed atm
#save detected objects in index to be output. video is not necessary
#change data from stream output to array ^
