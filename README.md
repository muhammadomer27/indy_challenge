INDY Challenge Vision Models Scripts

# Version 1
Date : 27-02-2025
Description : This code is for reading the camera topic from a mcap file , infer on it using a YOLO V11 model and get the output bounding box and classes from it. The code also generates an output video with the detections.

>Note:  The following code waas tested and confirmed to be working on a system with the following specification:
> 
>- OS : Ubuntu 22.04.5 LTS  
>- GPU :NVIDIA GeForce RTX 3080, 16 GB  
>- Nvidia Driver Version : 550.127.05   
>- Nvidia Cuda Version : 12.4  
>- Python : 3.10.12

# Usage Instructions: 
1. Make sure nvidia drivers and cuda are installed.
2. Setup environment using the requirements file.
3. Keep the required mcap files in input folder.
4. Run the python code inference.py
5. The output video will be generated as mp4 file and the detections are dumped as a list of list into a text file in the output folder. The detections will be dumpedinto the text file in the following format:
[frame
[2, ['car', 0.3310468792915344, [1189.7498779296875, 103.13622283935547, 1358.8409423828125, 173.78953552246094]]]
