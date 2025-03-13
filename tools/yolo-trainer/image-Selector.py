import os
import random
import shutil
import string

no_of_images = 1000
# Root directory containing all datasets
root_dir = "Frames"

# Output directory for selected images
selected_dir = "selectedImages"
os.makedirs(selected_dir, exist_ok=True)

# Collect all jpg images
image_paths = []
for subdir, _, files in os.walk(root_dir):
    for file in files:
        if file.lower().endswith(".jpg"):
            image_paths.append(os.path.join(subdir, file))

# Randomly select  images (or all if fewer than  exist)
selected_images = random.sample(image_paths, min(no_of_images, len(image_paths)))

# Function to generate a 6-character alphanumeric filename
def random_filename():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6)) + ".jpg"

# Copy selected images with random 6-character filenames
used_filenames = set()
for img_path in selected_images:
    new_name = random_filename()
    
    # Ensure unique filenames
    while new_name in used_filenames:
        new_name = random_filename()
    
    used_filenames.add(new_name)
    shutil.copy(img_path, os.path.join(selected_dir, new_name))

print(f"Copied {len(selected_images)} images to {selected_dir} with random 6-character names.")
