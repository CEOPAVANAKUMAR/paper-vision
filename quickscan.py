# ============================================================
#  Smart Image Scanner
#  Requirements: pip install opencv-python matplotlib numpy easyocr img2pdf
# ============================================================

import cv2
import numpy as np
import matplotlib.pyplot as plt
import easyocr
import img2pdf
import os

# ── CONFIG ───────────────────────────────────────────────────
# Change this to your image path
IMAGE_PATH = "images.png"          # <-- put your image path here
OUTPUT_JPG = "scanned_output.jpg"
OUTPUT_PDF = "scanned_output.pdf"
OUTPUT_TXT = "extracted_text.txt"
# ─────────────────────────────────────────────────────────────


def order_points(pts):
    """Order corner points: top-left, top-right, bottom-right, bottom-left."""
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]   # top-left
    rect[2] = pts[np.argmax(s)]   # bottom-right
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]  # top-right
    rect[3] = pts[np.argmax(diff)]  # bottom-left
    return rect


def show(title, img, cmap=None):
    """Helper to display an image."""
    plt.figure(figsize=(8, 6))
    plt.title(title)
    plt.imshow(img, cmap=cmap)
    plt.axis("off")
    plt.show()


# ── STEP 1: Load Image ───────────────────────────────────────
print("Loading image...")
img = cv2.imread(IMAGE_PATH)
if img is None:
    raise FileNotFoundError(f"Could not load image at: {IMAGE_PATH}")
print("Image shape:", img.shape)

original = img.copy()
show("Original Image", cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

# ── STEP 2: Grayscale ────────────────────────────────────────
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
show("Grayscale", gray, cmap="gray")

# ── STEP 3: Blur ─────────────────────────────────────────────
blur = cv2.GaussianBlur(gray, (5, 5), 0)
show("Blurred", blur, cmap="gray")

# ── STEP 4: Edge Detection ───────────────────────────────────
edges = cv2.Canny(blur, 75, 200)
show("Edges", edges, cmap="gray")

# ── STEP 5: Find Contours ────────────────────────────────────
contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
print(f"Contours found: {len(contours)}")

# ── STEP 6: Detect Document (4-sided polygon) ────────────────
screenCnt = None
for c in contours:
    perimeter = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * perimeter, True)
    if len(approx) == 4:
        screenCnt = approx
        break

if screenCnt is None:
    raise ValueError("Could not detect a 4-sided document in the image. "
                     "Try adjusting the Canny thresholds (75, 200).")
print("Document corners:\n", screenCnt)

# ── STEP 7: Draw Detected Border ─────────────────────────────
img_bordered = img.copy()
cv2.drawContours(img_bordered, [screenCnt], -1, (0, 255, 0), 3)
show("Detected Document Border", cv2.cvtColor(img_bordered, cv2.COLOR_BGR2RGB))

# ── STEP 8: Perspective Warp ─────────────────────────────────
pts = screenCnt.reshape(4, 2)
rect = order_points(pts)
tl, tr, br, bl = rect

widthA  = np.linalg.norm(br - bl)
widthB  = np.linalg.norm(tr - tl)
maxWidth = max(int(widthA), int(widthB))

heightA  = np.linalg.norm(tr - br)
heightB  = np.linalg.norm(tl - bl)
maxHeight = max(int(heightA), int(heightB))

dst = np.array(
    [[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]],
    dtype="float32"
)

M    = cv2.getPerspectiveTransform(rect, dst)
warp = cv2.warpPerspective(original, M, (maxWidth, maxHeight))
show("Warped / Cropped", cv2.cvtColor(warp, cv2.COLOR_BGR2RGB))

# ── STEP 9: Adaptive Threshold (Scanner Effect) ──────────────
gray_warp = cv2.cvtColor(warp, cv2.COLOR_BGR2GRAY)
scan = cv2.adaptiveThreshold(
    gray_warp, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY, 11, 2
)
show("Scanned (B&W)", scan, cmap="gray")

# ── STEP 10: Save JPG ────────────────────────────────────────
cv2.imwrite(OUTPUT_JPG, scan)
print(f"Image saved → {OUTPUT_JPG}")

# ── STEP 11: Create PDF ──────────────────────────────────────
with open(OUTPUT_PDF, "wb") as f:
    f.write(img2pdf.convert(OUTPUT_JPG))
print(f"PDF saved  → {OUTPUT_PDF}")

# ── STEP 12: OCR Text Extraction ─────────────────────────────
print("Running OCR (this may take a moment)...")
reader = easyocr.Reader(['en'])
result = reader.readtext(OUTPUT_JPG)

print("\n── Extracted Text ──────────────────────")
extracted = ""
for r in result:
    print(r[1])
    extracted += r[1] + " "

# ── STEP 13: Save Extracted Text ─────────────────────────────
with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
    f.write(extracted)
print(f"\nText saved → {OUTPUT_TXT}")

# ── FINAL CHECK ──────────────────────────────────────────────
print("\n── Summary ─────────────────────────────")
print("Smart Image Scanner completed successfully!")
print(f"PDF created   : {os.path.exists(OUTPUT_PDF)}")
print(f"Text created  : {os.path.exists(OUTPUT_TXT)}")
