import os
import shutil
import random
import string

# Define paths
source_dir = "selectedImages"  # Update this to your input folder
dest_root = "dataset"  # Update this to your destination folder

# Define destination directories
image_train_dir = os.path.join(dest_root, "images/train")
image_val_dir = os.path.join(dest_root, "images/val")
label_train_dir = os.path.join(dest_root, "labels/train")
label_val_dir = os.path.join(dest_root, "labels/val")

# Create necessary directories
for dir_path in [image_train_dir, image_val_dir, label_train_dir, label_val_dir]:
    os.makedirs(dir_path, exist_ok=True)

# Function to generate a random name (3 letters + 3 digits)
def generate_random_name():
    letters = ''.join(random.choices(string.ascii_uppercase, k=3))
    numbers = ''.join(random.choices(string.digits, k=3))
    return letters + numbers

# Get all JPG files in the source directory
jpg_files = [f for f in os.listdir(source_dir) if f.endswith(".jpg")]

# Rename files randomly while keeping pairs intact
renamed_files = []
for file in jpg_files:
    old_img_path = os.path.join(source_dir, file)
    old_txt_path = os.path.join(source_dir, file.replace(".jpg", ".txt"))

    # Generate a unique random name
    new_name = generate_random_name()

    # Ensure uniqueness
    while new_name in renamed_files:
        new_name = generate_random_name()
    
    renamed_files.append(new_name)

    new_img_path = os.path.join(source_dir, new_name + ".jpg")
    new_txt_path = os.path.join(source_dir, new_name + ".txt")

    # Rename image
    #os.rename(old_img_path, new_img_path)

    # Rename label if it exists
    #if os.path.exists(old_txt_path):
    #    os.rename(old_txt_path, new_txt_path)

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
