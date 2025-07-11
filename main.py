import os
import fitz  # PyMuPDF
import pytesseract
from PIL import Image, ImageDraw, ImageFont


PDF_FILE_PATH = "./data/aluminum_hinge.pdf"
OUTPUT_DIR = "./translated_specs"
DEFAULT_FONT_PATH = "./NotoSansSC-Regular.ttf"

def get_optimal_font(
    text, font_path, bbox_width, bbox_height
):
    """
    Calculates the optimal font and size to fit text within a bounding box.
    It prioritizes fitting the width first, then adjusts for height.
    """
    try:
        # Start with a font size that is a bit smaller than the bbox height
        # This is a much better starting guess than a fixed number.
        font_size = int(bbox_height * 0.9)
        font = ImageFont.truetype(font_path, font_size)

        # 1. Adjust for Width: Shrink font size until text width fits
        while font.getbbox(text)[2] > bbox_width and font_size > 1:
            font_size -= 1
            font = ImageFont.truetype(font_path, font_size)

        # 2. Adjust for Height: Further shrink if height is still too big
        while (font.getbbox(text)[3] - font.getbbox(text)[1]) > bbox_height and font_size > 1:
            font_size -= 1
            font = ImageFont.truetype(font_path, font_size)

        return font

    except IOError:
        print(
            f"Warning: Could not load font '{font_path}'. Using default."
        )
        # Fallback to a default font that is likely to be very small
        return ImageFont.load_default()


def process_pdf(pdf_path, output_dir):
    """
    Processes a PDF file: extracts images, performs OCR, translates text,
    and saves the annotated images.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    doc = fitz.open(pdf_path)
    print(f"Processing {len(doc)} pages from '{pdf_path}'...")

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        # *** CHANGE 1: Use a reasonable DPI ***
        pix = page.get_pixmap(dpi=1200)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        print(f"  - Page {page_num + 1}: Performing OCR...")
        ocr_data = pytesseract.image_to_data(
            img,
            lang="eng",
            output_type=pytesseract.Output.DICT,
            config="--oem 1 --psm 3", # Removed blacklist for more general use
        )

        draw = ImageDraw.Draw(img)
        num_boxes = len(ocr_data["level"])

        for i in range(num_boxes):
            # Use a slightly lower confidence to catch more text if needed
            if int(ocr_data["conf"][i]) > 10:
                text = ocr_data["text"][i]
                if text.strip():
                    (x, y, w, h) = (
                        ocr_data["left"][i],
                        ocr_data["top"][i],
                        ocr_data["width"][i],
                        ocr_data["height"][i],
                    )

                    # Placeholder for actual translation
                    translated_text = "企鹅"

                    # *** CHANGE 2: Use the new, smarter font sizing function ***
                    target_font = get_optimal_font(
                        translated_text, DEFAULT_FONT_PATH, w, h
                    )

                    # Erase the old text
                    draw.rectangle(
                        [x, y, x + w, y + h], fill="white", outline="white"
                    )

                    # *** CHANGE 3: Improved vertical centering ***
                    # Use textbbox which is more accurate for positioning
                    text_bbox = draw.textbbox(
                        (x, y), translated_text, font=target_font
                    )
                    text_height = text_bbox[3] - text_bbox[1]
                    
                    # Calculate position to center the new text in the old box
                    text_y = y + (h - text_height) / 2
                    
                    draw.text(
                        (x, text_y),
                        translated_text,
                        fill="black",
                        font=target_font,
                    )

        output_image_path = os.path.join(
            output_dir, f"page_{page_num + 1}_translated.png"
        )
        img.save(output_image_path)
        print(f"  - Saved translated page to '{output_image_path}'\n")

    doc.close()
    print("Processing complete.")


if __name__ == "__main__":
    if not os.path.exists(PDF_FILE_PATH):
        print(f"Error: Input PDF file not found at '{PDF_FILE_PATH}'")
    else:
        process_pdf(PDF_FILE_PATH, OUTPUT_DIR)
