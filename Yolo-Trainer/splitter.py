import os
import shutil
import random

# Define paths
source_dir = "TrainingData"  # Update this to your input folder
dest_root = "dataset"  # Update this to your destination folder

# Define destination directories
image_train_dir = os.path.join(dest_root, "images/train")
image_val_dir = os.path.join(dest_root, "images/val")
label_train_dir = os.path.join(dest_root, "labels/train")
label_val_dir = os.path.join(dest_root, "labels/val")

# Create necessary directories
for dir_path in [image_train_dir, image_val_dir, label_train_dir, label_val_dir]:
    os.makedirs(dir_path, exist_ok=True)

# Get updated list of renamed JPG files
jpg_files = [f for f in os.listdir(source_dir) if f.endswith(".jpg")]

# Shuffle and split files (80% train, 20% val)
random.shuffle(jpg_files)
split_index = int(0.8 * len(jpg_files))

train_files = jpg_files[:split_index]
val_files = jpg_files[split_index:]

# Function to copy files
def copy_files(files, src_folder, dest_img_folder, dest_label_folder):
    for file in files:
        img_src_path = os.path.join(src_folder, file)
        label_src_path = os.path.join(src_folder, file.replace(".jpg", ".txt"))

        img_dest_path = os.path.join(dest_img_folder, file)
        label_dest_path = os.path.join(dest_label_folder, file.replace(".jpg", ".txt"))

        # Copy image
        shutil.copy(img_src_path, img_dest_path)

        # Copy corresponding label if it exists
        if os.path.exists(label_src_path):
            shutil.copy(label_src_path, label_dest_path)

# Copy files to respective folders
copy_files(train_files, source_dir, image_train_dir, label_train_dir)
copy_files(val_files, source_dir, image_val_dir, label_val_dir)

print(f"Renaming & Split completed: {len(train_files)} images in train, {len(val_files)} images in val.")
