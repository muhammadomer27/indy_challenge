
from ultralytics import YOLO # For 

import torch

import rosbag2_py  # For reading mcap files
from rclpy.serialization import deserialize_message # For deserializing the messages
from rosidl_runtime_py.utilities import get_message # For extracting the messages frm the topics
from cv_bridge import CvBridge # For converting camera messages into opencv format
import cv2 # For image processing

import os
from pathlib import Path

import gc # For gabage collection and freeing up memory
import warnings

warnings.filterwarnings("ignore")


class infer():

    def __init__(self):
        """ Model Initialization """
        try:
            self.model = YOLO("./weights/yolo-11-m-v1.pt")
            self.model.to('cuda')
            self.classNames = self.model.names

            self.bridge = CvBridge()
            self.reader = rosbag2_py.SequentialReader()
        except Exception as e:
            print(e)
        

    def cleanUp(self):
        """ Cleans up resources """

        del self.model
        torch.cuda.empty_cache() 
        gc.collect()
        del self.reader
        self.frontVideo.release()
        self.rearVideo.release()
        self.leftVideo.release()
        self.rightVideo.release()
        self.stereo_leftVideo.release()
        self.stereo_rightVideo.release()
        self.frontTxt.close()
        self.rearTxt.close()
        self.leftTxt.close()
        self.rightTxt.close()
        self.stereoLeftTxt.close()
        self.stereoRightTxt.close()

        print("******** Completed **********")

    def loadMcap(self,inputBag):
        """ Reads the mcap file, detection text file writer and Video writer initialization """

        try:
            self.frameCount = 1
            inputPath = "./input/"+str(inputBag)
            self.outputLoc = "./output/"+str(inputBag).split(".")[0]
            Path(self.outputLoc).mkdir(parents=True,exist_ok=True)

            # Different cameras have different resolutions. Hence the output videeo will be having different resolutions as well.
            self.frontVideo = cv2.VideoWriter(self.outputLoc+"/front.mp4",cv2.VideoWriter_fourcc(*'mp4v'),25,(2064,400))
            self.rearVideo = cv2.VideoWriter(self.outputLoc+"/rear.mp4",cv2.VideoWriter_fourcc(*'mp4v'),25,(2064,400))
            self.leftVideo = cv2.VideoWriter(self.outputLoc+"/left.mp4",cv2.VideoWriter_fourcc(*'mp4v'),25,(2064,500))
            self.rightVideo = cv2.VideoWriter(self.outputLoc+"/right.mp4",cv2.VideoWriter_fourcc(*'mp4v'),25,(2064,500))
            self.stereo_leftVideo = cv2.VideoWriter(self.outputLoc+"/stereo_left.mp4",cv2.VideoWriter_fourcc(*'mp4v'),25,(2064,760))
            self.stereo_rightVideo = cv2.VideoWriter(self.outputLoc+"/stereo_right.mp4",cv2.VideoWriter_fourcc(*'mp4v'),25,(2064,760))

            self.frontTxt = open(self.outputLoc+"/front.txt", "w")
            self.rearTxt = open(self.outputLoc+"/rear.txt", "w")
            self.leftTxt = open(self.outputLoc+"/left.txt", "w")
            self.rightTxt = open(self.outputLoc+"/right.txt", "w")
            self.stereoLeftTxt = open(self.outputLoc+"/stereo_left.txt", "w")
            self.stereoRightTxt = open(self.outputLoc+"/stereo_right.txt", "w")


            self.reader.open(
                rosbag2_py.StorageOptions(uri=inputPath, storage_id="mcap"),
                rosbag2_py.ConverterOptions(input_serialization_format="cdr", output_serialization_format="cdr"),)

            self.topic_types = self.reader.get_all_topics_and_types()
        except Exception as e:
            print(e)
    
   
    def topicTypeName(self,topic_name):
        """ Get Topic Names """

        for topic_type in self.topic_types:
            if topic_type.name == topic_name:
                return topic_type.type
        raise ValueError(f"topic {topic_name} not in bag") 



    def inferandWWrite(self,message,view):
        """ Infer on camera messages and write them to video files """

        cv2_image = self.bridge.imgmsg_to_cv2(message,"bgr8")
        results = self.model(cv2_image,conf=0.3,verbose=False)
        annotatedFrame = results[0].plot()

        detections = []
        
        for result in results:
            for box in result.boxes:
                name = self.classNames[int(box.cls)]
                conf, boxes = box.conf.cpu().numpy()[0].tolist(), box.xyxy.cpu().numpy()[0].tolist()
                detections.append([name, conf, boxes])
    
        detections = str(detections)    

        if view=="front":
            self.frontVideo.write(annotatedFrame)
            self.frontTxt.write(detections+ '\n')
        elif view=="rear":
            self.rearVideo.write(annotatedFrame)
            self.rearTxt.write(detections+ '\n')
        elif view=="left":
            self.leftVideo.write(annotatedFrame)
            self.leftTxt.write(detections+ '\n')
        elif view=="right":
            self.rightVideo.write(annotatedFrame)
            self.rightTxt.write(detections+ '\n')
        elif view=="stereo_left":
            self.stereo_leftVideo.write(annotatedFrame)
            self.stereoLeftTxt.write(detections+ '\n')
        elif view=="stereo_right":
            self.stereo_rightVideo.write(annotatedFrame)
            self.stereoRightTxt.write(detections+ '\n')

        

    def extraction(self):
        """ Extracts camera messages from available topics """

        topicList = ["/sensors/camera/front/image","/sensors/camera/rear/image",
                     "/sensors/camera/left/image","/sensors/camera/right/image",
                     "/sensors/camera/stereo_left/image","/sensors/camera/stereo_right/image"]
        while self.reader.has_next():
            topic, data, _ = self.reader.read_next()
            if topic in topicList:
                view = topic.split("/")[3]
                msg_type = get_message(self.topicTypeName(topic))
                msg = deserialize_message(data, msg_type)
                self.inferandWWrite(msg,view)

                
        self.cleanUp()
    


if __name__ == "__main__":

    folder = Path("input")
    for file in folder.rglob("*.mcap"):
        print("Processing {}".format(str(file).split("/")[1]))
        inferObject = infer()
        inferObject.loadMcap(str(file).split("/")[1])
        inferObject.extraction()
        del inferObject




