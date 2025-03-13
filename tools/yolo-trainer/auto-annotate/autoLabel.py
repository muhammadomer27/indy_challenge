from ultralytics.data.annotator import auto_annotate

# auto_annotate(data="../selectedImages", det_model="<model-name>.pt", sam_model="mobile_sam.pt",device="cuda",conf=0.2)

auto_annotate(data="../selectedImages", det_model="1234-remix-kaist.pt", sam_model="mobile_sam.pt",device="cuda",conf=0.2)
