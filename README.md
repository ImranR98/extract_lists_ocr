# extract_lists_ocr

Uses EasyOCR to detect lists of words in images.

Usage:
1. Prep: `mkdir -p images && mkdir -p models`
2. Build Docker image: `docker build -t extract_lists_ocr_latest .`
3. Place OCR images into `./images`
4. Run: `docker run --rm -it -v ./images:/images -v ./models:/models extract_lists_ocr_latest:latest`
5. Results are saved as text files in `./images`

> Project abandoned as the results turned out to be totally inaccurate for my use case (handwritten lists).