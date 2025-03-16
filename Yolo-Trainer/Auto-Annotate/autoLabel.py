from ultralytics.data.annotator import auto_annotate

auto_annotate(data="../selectedImages", det_model="../../Models/yolo-11-m-v5.pt", sam_model="mobile_sam.pt",device="cuda",conf=0.2)
