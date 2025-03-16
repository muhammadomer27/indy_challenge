# Steps to Run

1. Make sure you have installed Pytorch with Cuda in your system.

2. If required, modify the python version/path inside replaceAnnotateFunction.sh

3. Run the following commands to replace the function from Ultralytics to get the output in the required format.
```
chmod +x replaceAnnotateFunction.sh
./replaceAnnotateFunction.sh
```

4. Keep the Object detection model in the **auto-annotate** folder. The Sam model will be automatically downloaded.

5. Modify model name and confidence inside **autoLabel.py** if required.

6. Run 
```
python3 autoLabel.py
```

7. The labels will be generated in a folder named **selectedImages_auto_annotated** in the same location as **selectedimages**
