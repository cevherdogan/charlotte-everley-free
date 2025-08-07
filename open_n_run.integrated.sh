echo if http-server .
echo then open http://localhost:8080/charlotteeverley-site/gallery.generated.html

echo if http-server charlotteeverley-site/
echo open http://localhost:8080/gallery.generated.html

open charlotteeverley-site/gallery.generated.html  # veya
http://localhost:8080/gallery.generated.html

http-server charlotteeverley-site/

