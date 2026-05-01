import fitz  # PyMuPDF
import os
import time

# -------------------------------

# ⚙️ CONFIGURATION (EDIT HERE)
# -------------------------------
# 👉 ENTER MAIN INPUT ROOT FOLDER (contains PDFs + subfolders)
INPUT_ROOT = "input_root"  # Change as needed
# 👉 ENTER MAIN OUTPUT ROOT FOLDER (images will be saved here, structure mirrored)
OUTPUT_ROOT = "output_root"  # Change as needed
# 👉 OPTIONAL SETTINGS
ZOOM = 2.0        # Image quality (higher = better quality, larger size)
VERBOSE = True    # False = silent mode


# -------------------------------
# Utility Function
# -------------------------------
def get_all_pdfs_recursive(folder):
    """Scan folder and subfolders for PDFs"""
    pdf_files = []

    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))

    return pdf_files


# -------------------------------
# Core Function
# -------------------------------
def extract_manga_pages(
    pdf_path,
    output_folder,
    zoom=2.0,
    verbose=True
):
    os.makedirs(output_folder, exist_ok=True)
    filename = os.path.basename(pdf_path)
    manga_name = os.path.splitext(filename)[0]
    manga_output_dir = os.path.join(output_folder, manga_name)
    os.makedirs(manga_output_dir, exist_ok=True)
    stats = {
        "total_pdfs": 1,
        "processed_pdfs": 0,
        "total_pages": 0,
        "errors": []
    }
    start_time = time.time()
    if verbose:
        print(f"📄 Processing: {manga_name}...")
    try:
        doc = fitz.open(pdf_path)
        num_pages = len(doc)
        padding = len(str(num_pages))
        for page_index in range(num_pages):
            page = doc.load_page(page_index)
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat, colorspace=fitz.csRGB)
            page_num = str(page_index + 1).zfill(padding)
            image_filename = f"{manga_name}_page_{page_num}.jpg"
            pix.save(os.path.join(manga_output_dir, image_filename))
            stats["total_pages"] += 1
        doc.close()
        stats["processed_pdfs"] += 1
        if verbose:
            print(f"✅ Done: {manga_name} ({num_pages} pages)")
    except Exception as e:
        print(f"❌ Error: {filename} -> {e}")
        stats["errors"].append(f"{filename}: {str(e)}")
    duration = round(time.time() - start_time, 2)
    if verbose:
        print("\n" + "=" * 40)
        print("📊 JOB SUMMARY")
        print("=" * 40)
        print(f"Status:        {'SUCCESS' if not stats['errors'] else 'WITH ERRORS'}")
        print(f"Time:          {duration}s")
        print(f"PDFs Found:    {stats['total_pdfs']}")
        print(f"PDFs Done:     {stats['processed_pdfs']}")
        print(f"Images Made:   {stats['total_pages']}")
        if stats["errors"]:
            print("-" * 40)
            print("ERRORS:")
            for err in stats["errors"]:
                print(f"  - {err}")
        print("=" * 40)


# -------------------------------
# 🚀 RUN SCRIPT
# -------------------------------
def process_all_pdfs(input_root, output_root, zoom=2.0, verbose=True):
    for current_dir, dirs, files in os.walk(input_root):
        rel_dir = os.path.relpath(current_dir, input_root)
        output_dir = os.path.join(output_root, rel_dir)
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_path = os.path.join(current_dir, file)
                extract_manga_pages(
                    pdf_path=pdf_path,
                    output_folder=output_dir,
                    zoom=zoom,
                    verbose=verbose
                )


if __name__ == "__main__":
    process_all_pdfs(
        input_root=INPUT_ROOT,
        output_root=OUTPUT_ROOT,
        zoom=ZOOM,
        verbose=VERBOSE
    )

    if verbose:
        print(f"🚀 Found {len(pdf_files)} PDFs (including subfolders)")
        print("-" * 40)

    for pdf_path in pdf_files:
        filename = os.path.basename(pdf_path)
        manga_name = os.path.splitext(filename)[0]

        manga_output_dir = os.path.join(output_folder, manga_name)
        os.makedirs(manga_output_dir, exist_ok=True)

        if verbose:
            print(f"📄 Processing: {manga_name}...")

        try:
            doc = fitz.open(pdf_path)
            num_pages = len(doc)
            padding = len(str(num_pages))

            for page_index in range(num_pages):
                page = doc.load_page(page_index)

                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat, colorspace=fitz.csRGB)

                page_num = str(page_index + 1).zfill(padding)
                image_filename = f"{manga_name}_page_{page_num}.jpg"

                pix.save(os.path.join(manga_output_dir, image_filename))
                stats["total_pages"] += 1

            doc.close()
            stats["processed_pdfs"] += 1

            if verbose:
                print(f"✅ Done: {manga_name} ({num_pages} pages)")

        except Exception as e:
            print(f"❌ Error: {filename} -> {e}")
            stats["errors"].append(f"{filename}: {str(e)}")

    duration = round(time.time() - start_time, 2)

    if verbose:
        print("\n" + "=" * 40)
        print("📊 JOB SUMMARY")
        print("=" * 40)
        print(f"Status:        {'SUCCESS' if not stats['errors'] else 'WITH ERRORS'}")
        print(f"Time:          {duration}s")
        print(f"PDFs Found:    {stats['total_pdfs']}")
        print(f"PDFs Done:     {stats['processed_pdfs']}")
        print(f"Images Made:   {stats['total_pages']}")

        if stats["errors"]:
            print("-" * 40)
            print("ERRORS:")
            for err in stats["errors"]:
                print(f"  - {err}")
        print("=" * 40)


# -------------------------------
# 🚀 RUN SCRIPT
# -------------------------------
if __name__ == "__main__":
    extract_manga_pages(
        input_folder=INPUT_FOLDER,
        output_folder=OUTPUT_FOLDER,
        zoom=ZOOM,
        verbose=VERBOSE
    )