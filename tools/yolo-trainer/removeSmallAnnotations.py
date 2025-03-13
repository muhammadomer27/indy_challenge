import os
from PIL import Image

# New image dimensions after resizing
newWidth, newHeight = 640, 640
thresholdArea = 300  # Minimum area after resizing

# Directories
annotationsDir = "labels"
imagesDir = "images"
outputDir = "filtered_annotations"
os.makedirs(outputDir, exist_ok=True)

def filterAnnotations(filePath, outputPath, imagePath):
    # Get original image size
    with Image.open(imagePath) as img:
        origWidth, origHeight = img.size
    
    with open(filePath, "r") as f:
        lines = f.readlines()
    
    filteredLines = []
    for line in lines:
        parts = line.strip().split()
        classId, xCenter, yCenter, width, height = parts[0], float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])
        
        # Process only class 0 and class 1
        if classId not in ["0", "1"]:
            continue
        
        # Convert to absolute dimensions
        absWidth = width * origWidth
        absHeight = height * origHeight
        
        # Resize bounding box
        resizedWidth = absWidth * (newWidth / origWidth)
        resizedHeight = absHeight * (newHeight / origHeight)
        
        # Filter based on area
        if resizedWidth * resizedHeight >= thresholdArea:
            filteredLines.append(f"{classId} {xCenter} {yCenter} {width} {height}\n")
    
    # Write filtered annotations
    with open(outputPath, "w") as f:
        f.writelines(filteredLines)

def processAnnotations():
    for filename in os.listdir(annotationsDir):
        if filename.endswith(".txt"):
            inputPath = os.path.join(annotationsDir, filename)
            imagePath = os.path.join(imagesDir, filename.replace(".txt", ".jpg"))  # Adjust if image format is different
            outputPath = os.path.join(outputDir, filename)
            
            if os.path.exists(imagePath):
                filterAnnotations(inputPath, outputPath, imagePath)
                print(f"Processed {filename}")
            else:
                print(f"Image not found for {filename}, skipping...")

if __name__ == "__main__":
    processAnnotations()
    print("Filtering complete!")
