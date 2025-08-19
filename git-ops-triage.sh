# 1) Show HEAD vs working-tree sizes & hashes
for f in \
  sb/gallery_quickstart/assets/images/raw/devon-og.jpg \
  sb/gallery_quickstart/assets/images/raw/key-considerations.png \
  sb/gallery_quickstart/assets/images/raw/mainline-demographics.png \
  sb/gallery_quickstart/assets/images/raw/tracks-of-legacy.png \
  sb/gallery_quickstart/assets/images/raw/tracks-through-time.png \
  sb/gallery_quickstart/assets/images/raw/valleyforge-memorial-gardens.png
do
  echo "=== $f"
  git show HEAD:"$f" > /tmp/_head
  shasum /tmp/_head | awk '{print "HEAD   sha1:",$1}'
  stat -f "HEAD   size: %z" /tmp/_head 2>/dev/null || stat -c "HEAD   size: %s" /tmp/_head

  shasum "$f"       | awk '{print "WORK   sha1:",$1}'
  stat -f "WORK   size: %z" "$f" 2>/dev/null || stat -c "WORK   size: %s" "$f"

  # If you have exiftool & imagemagick installed, these help:
  command -v exiftool >/dev/null && { echo "-- EXIF delta (HEAD vs WORK)"; exiftool -s -FileType -ColorSpace -ICC_Profile:all /tmp/_head 2>/dev/null; exiftool -s -FileType -ColorSpace -ICC_Profile:all "$f" 2>/dev/null; }
  echo
done


