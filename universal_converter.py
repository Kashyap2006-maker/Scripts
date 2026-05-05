import sys
import os
import mimetypes

# Import libraries for conversions
try:
    from PIL import Image
except ImportError:
    Image = None
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None
try:
    import docx
except ImportError:
    docx = None
try:
    import pandas as pd
except ImportError:
    pd = None

# Add more imports as needed

def convert_file(input_path, output_path):
    input_ext = os.path.splitext(input_path)[1].lower()
    output_ext = os.path.splitext(output_path)[1].lower()
    
    # Image conversions (lossless when possible)
    image_exts = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
    if input_ext in image_exts and output_ext in image_exts + ['.pdf']:
        if not Image:
            print("Pillow is required for image conversions. Please install it.")
            return
        img = Image.open(input_path)
        # Warn if converting from lossless to lossy
        lossless_exts = ['.png', '.bmp', '.tiff']
        lossy_exts = ['.jpg', '.jpeg']
        if input_ext in lossless_exts and output_ext in lossy_exts:
            print(f"Warning: Converting from {input_ext} (lossless) to {output_ext} (lossy) may reduce quality.")
        # Save with max quality for JPEG
        save_kwargs = {}
        if output_ext in ['.jpg', '.jpeg']:
            save_kwargs['quality'] = 100
            save_kwargs['subsampling'] = 0
            save_kwargs['optimize'] = True
        if output_ext == '.png':
            save_kwargs['compress_level'] = 0  # No compression, lossless
        if output_ext == '.pdf':
            img.save(output_path, 'PDF', **save_kwargs)
        else:
            img.save(output_path, **save_kwargs)
        print(f"Converted {input_path} to {output_path} (max quality settings)")
        return
    
    # PDF to image (first page, lossless if possible)
    if input_ext == '.pdf' and output_ext in image_exts:
        try:
            from pdf2image import convert_from_path
        except ImportError:
            print("pdf2image is required for PDF to image conversion. Please install it.")
            return
        images = convert_from_path(input_path)
        save_kwargs = {}
        if output_ext in ['.jpg', '.jpeg']:
            save_kwargs['quality'] = 100
            save_kwargs['subsampling'] = 0
            save_kwargs['optimize'] = True
        if output_ext == '.png':
            save_kwargs['compress_level'] = 0
        images[0].save(output_path, **save_kwargs)
        print(f"Converted first page of {input_path} to {output_path} (max quality settings)")
        return
    
    # CSV to JSON
    if input_ext == '.csv' and output_ext == '.json':
        if not pd:
            print("pandas is required for CSV/JSON conversions. Please install it.")
            return
        df = pd.read_csv(input_path)
        df.to_json(output_path, orient='records', lines=True, force_ascii=False)
        print(f"Converted {input_path} to {output_path} (lossless data conversion)")
        return

    # JSON to CSV
    if input_ext == '.json' and output_ext == '.csv':
        if not pd:
            print("pandas is required for CSV/JSON conversions. Please install it.")
            return
        df = pd.read_json(input_path, lines=True)
        df.to_csv(output_path, index=False)
        print(f"Converted {input_path} to {output_path} (lossless data conversion)")
        return
    
    print(f"Conversion from {input_ext} to {output_ext} is not supported yet.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python universal_converter.py <input_file> <output_file>")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    convert_file(input_file, output_file)
