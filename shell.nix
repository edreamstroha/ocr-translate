with import <nixpkgs> {};

let
  ibm-watson-fixed = python3Packages.ibm-watson.overridePythonAttrs (oldAttrs: {
    doCheck = false;
  });
in

# CORRECTED: Call mkShell directly, not stdenv.mkShell
mkShell {
  name = "translation-env";

  buildInputs = [
    # The Python interpreter itself
    python3

    # The actual Tesseract OCR engine program
    tesseract

    # Your Python libraries
    python3Packages.pymupdf
    python3Packages.pytesseract
    python3Packages.pillow
    python3Packages.opencv-python-headless 
    python3Packages.numpy
  ];

  shellHook = ''

  if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
  fi

  source .venv/bin/activate

  pip install ibm-watsonx-ai
  '';
}
