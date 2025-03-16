from ultralytics import YOLO

# Load a pretrained YOLOv8 model
model = YOLO("yolo11m.pt")  # Use "yolov8s.pt", "yolov8m.pt", etc. for different sizes

# Train the model
model.train(
    data="./dataset/dataset.yaml",  # Path to data.yaml
    epochs=100,  # Number of training epochs
    imgsz=640,  # Image size
    batch=28,  # Adjust batch size based on GPU memory
    device="cuda",  # Use "cpu" if no GPU is available
    plots=True,
    degrees=3,
    translate=0.3,
    shear=0.2
)

