# YOLO-V8 Usage

**⭕ Source : https://github.com/marcoslucianops/DeepStream-Yolo**  

- [YOLO-V8 Usage](#yolo-v8-usage)
  - [1. ❇️ Env Setup ❇️](#1-️-env-setup-️)
  - [2. ❇️ Copy convertor script ❇️](#2-️-copy-convertor-script-️)
  - [3. ❇️ Copy the model ❇️](#3-️-copy-the-model-️)
  - [4. ❇️ Convert model ❇️](#4-️-convert-model-️)
  - [5. ❇️ Copy generated files ❇️](#5-️-copy-generated-files-️)
  - [6. ❇️ Compile the lib ❇️](#6-️-compile-the-lib-️)
  - [7. ❇️ Edit the config files as per the use case (if required)❇️](#7-️-edit-the-config-files-as-per-the-use-case-if-required️)


## 1. ❇️ Env Setup ❇️

```
git clone --branch v8.3.107 --depth 1 https://github.com/ultralytics/ultralytics.git 
cd ultralytics
sudo apt install python3-venv -y
python3 -m virtualenv ultralyticsenv
source ./ultralyticsenv/bin/activate
pip3 install -e .
pip3 install onnx onnxslim onnxruntime
```

## 2. ❇️ Copy convertor script ❇️

Copy the `export_yoloV8.py` file from `DeepStream-Yolo/utils` directory to the `ultralytics` folder.

```
cp ../DeepStream-Yolo/utils/export_yoloV8.py .
```

## 3. ❇️ Copy the model ❇️

⚠️⚠️ Make sure you have kept the custom trained Yolo-V8 model in `ultralytics` folder. 

## 4. ❇️ Convert model ❇️

Generate the ONNX model file.\
⚠️ For now run this command instead of the next two options.

```
python3 export_yoloV8.py -w yolo-v8m-iter1.pt
```

**NOTE**: ⭕ To use dynamic batch-size

```
python3 export_yoloV8.py -w yolo-v8m-iter1.pt --dynamic
```

**NOTE**: ⭕ To use static batch-size (example for batch-size = 4)

```
python3 export_yoloV8.py -w yolo-v8m-iter1.pt --batch 4
```
The file will be geenrated with the name **yolo-v8m-iter1.pt.onnx**

## 5. ❇️ Copy generated files ❇️

Copy the generated ONNX model file and labels.txt file (if generated) to the `DeepStream-Yolo` folder.

For example:
```
cp yolo-v8m-iter1.pt.onnx ../
cp labels.txt ../
```


## 6. ❇️ Compile the lib ❇️

 1. Go back to DeepStream-Yolo folder
  ```
  cd ../
  ```

2. Set the `CUDA_VER` according to your DeepStream version

```
export CUDA_VER=12.2
```

3. Make the lib

```
make -C nvdsinfer_custom_impl_Yolo clean && make -C nvdsinfer_custom_impl_Yolo
```

## 7. ❇️ Edit the config files as per the use case (if required)❇️

1. Edit the following lines in  `config_infer_primary_yoloV8.txt` in `configs` folder.
   
```
onnx-file=../yolo-v8m-iter1.pt.onnx
model-engine-file=../model_b1_gpu0_fp32.engine
labelfile-path=../labels.txt
....
....
num-detected-classes=2
.....
....
custom-lib-path=../nvdsinfer_custom_impl_Yolo/libnvdsinfer_custom_impl_Yolo.so
```

2. To change threshold and NMS values, modify the following lines in  `config_infer_primary_yoloV8.txt` in `configs` folder.
   
```
[class-attrs-all]
nms-iou-threshold=0.50
pre-cluster-threshold=0.50
```