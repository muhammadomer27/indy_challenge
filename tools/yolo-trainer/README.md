# Steps to Train a YOLO Model with Auto Annotaion to speed up the process.

## This folder contains various scripts for selecting images from dataset during training and validation.

```
!! The assumption here is that initially all the data is inside mcap files.
```


1. Keep your mcap files inside **mcap-Files** folder

2. Run **mcap-Frame-Extract.py** to extract allthe frames from mcap files. The  extracted frames will be kept in Frames folder.


4. Run **image-Selector.py** to select pre-defined no of images from your data or modify it at line no 6 .It'll save the selected images in **selectedImages** folder with random file names.

5. Go to **auto-annotate** folder, read the README there and set up everything as mentioned.

5. Go to **auto-annotate** folder and run **autoLabel.py** script. This will generated the annotations in the same directory as selectedImages.

5. (Optional) **removeSmallAnnotations.py** : Used to remove small bounding boxes of less than 300 pixels for default 640x640 yolo training.

6. To generate metrics for annotated validation data : 
    - Set confidence and IOU
    - Modify ./dataset/dataset.yaml 
```
yolo val model=<model path>.pt data=./dataset/dataset.yaml imgsz=640 batch=16 conf=0.5 iou=0.5 device=0
```

<Give absolute path of dataset folder> For example/home/mcap/labelStudio/yolotrainer/dataset/