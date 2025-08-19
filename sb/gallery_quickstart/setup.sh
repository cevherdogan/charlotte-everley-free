python3 -m venv .venv && source .venv/bin/activate
pip install pillow jinja2

# Build dev
ENV=dev \
DB_PATH=data/site.db \
IMG_RAW_DIR=assets/images/raw \
IMG_OUT_DIR=assets/images/thumbs \
OUTPUT_FILE=site/gallery.html \
python scripts/gallery/build_gallery.py

# Open the output
open site/gallery.html  # (macOS)  |  xdg-open site/gallery.html (Linux)

