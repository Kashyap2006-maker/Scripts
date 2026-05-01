import os
import shutil
import random
import time

# -------------------------------
# ⚙️ CONFIGURATION (EDIT HERE)
# -------------------------------

# 👉 ENTER MAIN SOURCE FOLDER (can contain subfolders)
SOURCE_DIRECTORY = "/path/to/your/source/folder"

# 👉 ENTER DESTINATION FOLDER
DESTINATION_DIRECTORY = "/path/to/save/random/images"

# 👉 NUMBER OF IMAGES TO SELECT
NUMBER_TO_SELECT = 100

# 👉 OPTIONAL SETTINGS
INCLUDE_SUBFOLDERS = True   # True = scan inside subfolders
VERBOSE = True              # False = silent mode


# -------------------------------
# Utility Function
# -------------------------------

def get_images_in_folder(folder):
    """Get all JPG/JPEG images in a single folder (not recursive)"""
    image_paths = []
    for file in os.listdir(folder):
        if file.lower().endswith(('.jpg', '.jpeg')):
            image_paths.append(os.path.join(folder, file))
    return image_paths


# -------------------------------
# Core Function
# -------------------------------

def select_random_images_in_folder(src_folder, dest_folder, count, verbose=True):
    os.makedirs(dest_folder, exist_ok=True)
    image_paths = get_images_in_folder(src_folder)
    if not image_paths:
        if verbose:
            print(f"❌ No images found in {src_folder}.")
        return
    actual_count = min(len(image_paths), count)
    if verbose:
        print(f"🎲 Found {len(image_paths)} images in {src_folder}")
        print(f"🎯 Selecting {actual_count} random images...")
    selected_files = random.sample(image_paths, actual_count)
    total_size_bytes = 0
    start_time = time.time()
    for i, src_path in enumerate(selected_files, 1):
        filename = os.path.basename(src_path)
        dest_path = os.path.join(dest_folder, filename)
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(dest_path):
            dest_path = os.path.join(dest_folder, f"{base}_{counter}{ext}")
            counter += 1
        total_size_bytes += os.path.getsize(src_path)
        shutil.copy2(src_path, dest_path)
        if verbose and (i % 10 == 0 or i == actual_count):
            print(f"🔄 {i}/{actual_count}", end="\r")
    duration = round(time.time() - start_time, 2)
    total_size_mb = total_size_bytes / (1024 * 1024)
    if verbose:
        print("\n" + "=" * 40)
        print("✅ DONE")
        print("=" * 40)
        print(f"Images Selected: {actual_count}")
        print(f"Time Taken:      {duration}s")
        print(f"Saved To:        {dest_folder}")
        print(f"Total Size:      {total_size_mb:.2f} MB")
        print("=" * 40)


# -------------------------------
# 🚀 RUN SCRIPT
# -------------------------------
# -------------------------------
# 🚀 RUN SCRIPT
# -------------------------------
def process_all_folders(input_root, output_root, count, verbose=True):
    for current_dir, dirs, files in os.walk(input_root):
        rel_dir = os.path.relpath(current_dir, input_root)
        output_dir = os.path.join(output_root, rel_dir)
        select_random_images_in_folder(
            src_folder=current_dir,
            dest_folder=output_dir,
            count=count,
            verbose=verbose
        )

if __name__ == "__main__":
    INPUT_ROOT = "input_root"  # Change as needed
    OUTPUT_ROOT = "output_root"  # Change as needed
    process_all_folders(
        input_root=INPUT_ROOT,
        output_root=OUTPUT_ROOT,
        count=NUMBER_TO_SELECT,
        verbose=VERBOSE
    )