# Steps to Run

1. Make sure you have installed Pytorch with Cuda in your system.

2. If required, modify the python version/path inside replaceAnnotateFunction.sh

3. Run the following commands to replace the function from Ultralytics to get the output in the required format.
```
chmod +x replaceAnnotateFunction.sh
./replaceAnnotateFunction.sh
```

4. Keep the Object detection model in the **auto-annotate** folder. The Sam model will be automatically downloaded.

5. Modify model name and confidence inside autoLabel.py
