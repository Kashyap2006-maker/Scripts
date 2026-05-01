import fitz  # PyMuPDF
import os
import re
import time

# -------------------------------

# ⚙️ CONFIGURATION (EDIT HERE)
# -------------------------------
# 👉 ENTER YOUR MAIN INPUT ROOT FOLDER (contains subfolders)
INPUT_ROOT = "input_root"  # Change as needed
# 👉 ENTER YOUR MAIN OUTPUT ROOT FOLDER (PDFs will be saved here, structure mirrored)
OUTPUT_ROOT = "output_root"  # Change as needed
# 👉 OPTIONAL SETTINGS
REVERSE_ORDER = False   # True = reverse order (useful for manga)
VERBOSE = True         # False = silent mode


# -------------------------------
# Utility Functions
# -------------------------------
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'([0-9]+)', s)]

def get_all_images_recursive(folder, extensions):
    """Scan folder and all subfolders for images"""
    image_paths = []

    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(extensions):
                image_paths.append(os.path.join(root, file))

    return image_paths


# -------------------------------
# Core Function
# -------------------------------

def convert_images_to_pdf(
    image_paths,
    output_pdf_path,
    reverse=False,
    verbose=True
):
    if not image_paths:
        if verbose:
            print(f"❌ No images found for PDF: {output_pdf_path}")
        return

    image_paths.sort(key=natural_sort_key, reverse=reverse)
    total_files = len(image_paths)
    processed_count = 0
    total_input_size = 0
    start_time = time.time()

    if verbose:
        print(f"🚀 Creating PDF: {output_pdf_path} ({total_files} images)")

    doc = fitz.open()

    for img_path in image_paths:
        total_input_size += os.path.getsize(img_path)
        try:
            imgdoc = fitz.open(img_path)
            pdfbytes = imgdoc.convert_to_pdf()
            imgdoc.close()
            img_pdf = fitz.open("pdf", pdfbytes)
            doc.insert_pdf(img_pdf)
            img_pdf.close()
            processed_count += 1
            if verbose and (processed_count % 5 == 0 or processed_count == total_files):
                print(f"🔄 {processed_count}/{total_files}", end="\r")
        except Exception as e:
            print(f"\n❌ Failed: {img_path} -> {e}")

    if processed_count == 0:
        if verbose:
            print(f"❌ No valid images to save for {output_pdf_path}")
        return

    if verbose:
        print("\n💾 Saving PDF...")
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
    doc.save(output_pdf_path, garbage=4, deflate=True)
    doc.close()
    duration = round(time.time() - start_time, 2)
    final_size = os.path.getsize(output_pdf_path)
    if verbose:
        print("\n" + "=" * 40)
        print("✅ DONE")
        print("=" * 40)
        print(f"Images:        {processed_count}/{total_files}")
        print(f"Time:          {duration}s")
        print(f"Output:        {output_pdf_path}")
        print(f"Input Size:    {total_input_size/(1024*1024):.2f} MB")
        print(f"PDF Size:      {final_size/(1024*1024):.2f} MB")
        print("=" * 40)


# -------------------------------
# 🚀 RUN SCRIPT
# -------------------------------
def process_all_folders(input_root, output_root, reverse=False, verbose=True):
    extensions = ('.jpg', '.jpeg', '.png', '.webp', '.tiff')
    for current_dir, dirs, files in os.walk(input_root):
        image_paths = [os.path.join(current_dir, f) for f in files if f.lower().endswith(extensions)]
        if image_paths:
            # Compute relative path from input_root
            rel_dir = os.path.relpath(current_dir, input_root)
            # Output PDF path mirrors input structure
            output_dir = os.path.join(output_root, rel_dir)
            output_pdf = os.path.join(output_dir, "images.pdf")
            convert_images_to_pdf(
                image_paths=image_paths,
                output_pdf_path=output_pdf,
                reverse=reverse,
                verbose=verbose
            )


if __name__ == "__main__":
    process_all_folders(
        input_root=INPUT_ROOT,
        output_root=OUTPUT_ROOT,
        reverse=REVERSE_ORDER,
        verbose=VERBOSE
    )


# -------------------------------
# 🚀 RUN SCRIPT
# -------------------------------
if __name__ == "__main__":
    convert_images_to_pdf(
        input_folder=INPUT_FOLDER,
        output_pdf_path=OUTPUT_PDF,
        reverse=REVERSE_ORDER,
        verbose=VERBOSE
    )