# PDF Image Text Processor (OCR & Text Overlay)

This project processes image-based PDF documents, extracts text using Optical Character Recognition (OCR), and then overlays new text (currently a placeholder translation) onto the original image. It's designed to handle design specifications where text might be embedded within images.

## Features

*   Extracts high-resolution images from PDF pages.
*   Performs OCR on extracted images to identify text and its bounding boxes.
*   Includes a function to dynamically size text to fit within original bounding boxes.
*   Overlays new text (e.g., translated text) onto the original image, replacing the OCR'd text.

## Setup Instructions (Ubuntu)

Follow these steps to get the project running on your Ubuntu system.

### 1. Prerequisites

Before you begin, ensure you have the following installed:

*   **Python 3.8+**:
    ```bash
    sudo apt update
    sudo apt install python3 python3-pip python3.10-venv
    ```
*   **Tesseract OCR Engine**:
    ```bash
    sudo apt install tesseract-ocr tesseract-ocr-eng
    ```
    (We only need the English language data for OCR, as the translation placeholder doesn't rely on Tesseract's Chinese capabilities.)

### 2. Download a Chinese Font

You need a font that supports Chinese characters for drawing the overlay text.

1.  Go to [Google Fonts](https://fonts.google.com/).
2.  Search for "Noto Sans SC" (Recommended).
3.  Download the font family.
4.  Extract the downloaded `.zip` file. Find the `NotoSansSC-Regular.ttf` file (or a similar `.ttf` or `.otf` file).
5.  **Place this font file in the root directory of your project (where your Python script is located).**
    *   **Important**: Ensure the filename matches what's in your Python script: `NotoSansSC-Regular.ttf`.

### 3. Project Setup

1.  **Clone this repository** (or create a new directory and put your Python script and `requirements.txt` inside it).
2.  **Navigate into the project directory** in your terminal.
3.  **Create and activate a Python virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
4.  **Install dependencies from `requirements.txt`:**
    ```bash
    pip install -r requirements.txt
    ```

    **(You will need to create the `requirements.txt` file yourself based on the Python script's imports. It should look like this:)**
    ```
    PyMuPDF
    pytesseract
    Pillow
    numpy
    ```

### 4. Configure Your Python Script

1.  Open your main Python script (e.g., `process_pdf.py`).
2.  Review the following paths and adjust if necessary:

    ```python
    PDF_FILE_PATH = "./data/aluminum_hinge.pdf"   # <--- Path to your input PDF
    OUTPUT_DIR = "./translated_specs"             # <--- Directory for output images
    DEFAULT_FONT_PATH = "./NotoSansSC-Regular.ttf" # <--- Ensure this matches your font file name and location
    ```
3.  The translation currently uses a placeholder: `translated_text = "企鹅"`. You would integrate your actual translation logic here in a later stage.

### 5. Prepare Your PDF

1.  Place the image-based PDF you want to process into the location specified by `PDF_FILE_PATH` (e.g., inside a `data` folder in your project root).

### 6. Run the Script

Once everything is configured:

```bash
python3 main.py
```

The script will process the PDF, perform OCR, replace the detected text with the placeholder, and save the resulting image files in the `translated_specs` directory.

## Important Notes

*   **OCR Quality:** The accuracy of the OCR depends heavily on the source PDF's image quality, resolution, and text clarity. The `dpi=1200` setting aims for high fidelity but consumes more memory.
*   **Font Fitting:** The `get_optimal_font` function attempts to best fit text within original bounding boxes, but complex layouts or very long translations might still lead to imperfect results.
*   **Actual Translation:** This version of the script uses a hardcoded placeholder for translation. To get real translations, you would integrate an external translation API (like IBM Watsonx.ai, Google Cloud Translate, etc.) into the `process_pdf` function.
