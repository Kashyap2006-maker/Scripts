import cv2
import os
import shutil
import time

# -------------------------------

# ⚙️ CONFIGURATION (EDIT HERE)
# -------------------------------
# 👉 ENTER MAIN INPUT ROOT FOLDER (can include subfolders)
INPUT_ROOT = "input_root"  # Change as needed
# 👉 ENTER MAIN OUTPUT ROOT FOLDER (selected images saved here, structure mirrored)
OUTPUT_ROOT = "output_root"  # Change as needed
# 👉 OPTIONAL SETTINGS
RESIZE_WINDOW = True        # True = resizable window
VERBOSE = True              # False = less logs


# -------------------------------
# Utility Function
# -------------------------------

def get_images_in_folder(folder):
    image_paths = []
    for file in os.listdir(folder):
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_paths.append(os.path.join(folder, file))
    return image_paths


# -------------------------------
# Core Function
# -------------------------------

def review_and_select_images_in_folder(
    source_folder,
    dest_folder,
    resize_window=True,
    verbose=True
):
    os.makedirs(dest_folder, exist_ok=True)
    image_paths = get_images_in_folder(source_folder)
    if not image_paths:
        if verbose:
            print(f"❌ No images found in {source_folder}.")
        return
    print(f"📸 Found {len(image_paths)} images in {source_folder}")
    print("Controls: 'y'=Save | 'n'=Skip | 'q'=Quit")
    print("-" * 40)
    count = 0
    total_size_bytes = 0
    start_time = time.time()
    if resize_window:
        cv2.namedWindow("Reviewing", cv2.WINDOW_NORMAL)
    for i, file_path in enumerate(image_paths, 1):
        filename = os.path.basename(file_path)
        img = cv2.imread(file_path)
        if img is None:
            continue
        cv2.imshow("Reviewing", img)
        key = cv2.waitKey(0) & 0xFF
        if key == ord('y'):
            dest_path = os.path.join(dest_folder, filename)
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(dest_path):
                dest_path = os.path.join(dest_folder, f"{base}_{counter}{ext}")
                counter += 1
            shutil.copy(file_path, dest_path)
            count += 1
            total_size_bytes += os.path.getsize(file_path)
            if verbose:
                print(f"[SAVED] {filename}")
        elif key == ord('n'):
            if verbose:
                print(f"[SKIPPED] {filename}")
        elif key == ord('q'):
            print("⛔ Stopped by user.")
            break
        if verbose:
            print(f"Progress: {i}/{len(image_paths)}", end="\r")
    cv2.destroyAllWindows()
    duration = round(time.time() - start_time, 2)
    total_size_mb = total_size_bytes / (1024 * 1024)
    print("\n" + "=" * 40)
    print("✅ COMPLETED")
    print("=" * 40)
    print(f"Selected Images: {count}")
    print(f"Time Taken:      {duration}s")
    print(f"Total Size:      {total_size_mb:.2f} MB")
    print(f"Saved To:        {dest_folder}")
    print("=" * 40)


# -------------------------------
# 🚀 RUN SCRIPT
# -------------------------------
def process_all_folders(input_root, output_root, resize_window=True, verbose=True):
    for current_dir, dirs, files in os.walk(input_root):
        rel_dir = os.path.relpath(current_dir, input_root)
        output_dir = os.path.join(output_root, rel_dir)
        review_and_select_images_in_folder(
            source_folder=current_dir,
            dest_folder=output_dir,
            resize_window=resize_window,
            verbose=verbose
        )

if __name__ == "__main__":
    process_all_folders(
        input_root=INPUT_ROOT,
        output_root=OUTPUT_ROOT,
        resize_window=RESIZE_WINDOW,
        verbose=VERBOSE
    )