# Smart Image Scanner

A Python-based document scanner that detects, crops, straightens, and extracts text from images using OpenCV and EasyOCR. Works on Google Colab — no local setup needed.

## Features

- Automatic document border detection
- Perspective warp to straighten angled photos
- Black & white scanner effect
- Exports scanned image as JPG and PDF
- OCR text extraction and saves to .txt file

## How to Run (Google Colab)

1. Open [Google Colab](https://colab.research.google.com) and create a new notebook
2. Paste the contents of `smart_scanner_fullpage.py` into a cell
3. Run the cell — it will:
   - Install all required libraries automatically
   - Ask you to upload your image
   - Process and scan the document
   - Download the output files to your computer

## Output Files

| File | Description |
|------|-------------|
| `scanned_output.jpg` | Black & white scanned image |
| `scanned_output.pdf` | PDF version of the scan |
| `extracted_text.txt` | OCR extracted text |

## Requirements

Install dependencies locally with:

```bash
pip install -r requirements.txt
```

Or run on Google Colab — libraries are installed automatically by the script.

## Run Locally

```bash
git clone https://github.com/your-username/smart-image-scanner.git
cd smart-image-scanner
pip install -r requirements.txt
python smart_scanner_fullpage.py
```

> Change `IMAGE_PATH` at the top of the script to point to your image file.

## Tech Stack

- [OpenCV](https://opencv.org/) — image processing & document detection
- [EasyOCR](https://github.com/JaidedAI/EasyOCR) — text extraction
- [img2pdf](https://github.com/josch/img2pdf) — PDF generation
- [Matplotlib](https://matplotlib.org/) — image display
- [NumPy](https://numpy.org/) — numerical operations

## Project Structure

```
smart-image-scanner/
├── smart_scanner_fullpage.py   # Main scanner script
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

## License

MIT License — free to use and modify.
