echo """

find . -name gallery.html -print
./articles/gallery.html
./charlotteeverley-site/gallery.html
"""

echo "Open in another terminal:"
echo "open http://localhost:8000/charlotteeverley-site/gallery.html"

python3 -m http.server 8000

