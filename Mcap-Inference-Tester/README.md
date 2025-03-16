# MCAP File Inference Tester

Description : This code is for reading the camera topic from a mcap file , infer on it using a YOLO V11 model and get the output bounding box and classes from it. The code also generates an output video with the detections.

## Usage Instructions

1. Keep the required mcap files in input folder.
2. Run the python code **inference.py**
3. The output video will be generated as mp4 file and the detections are dumped as a list of list into a text file in the output folder. The detections will be dumped into the text file in the following format:

   **[ [class,confidence,[bounding box]] , [class,confidence,[bounding box]] ]**


