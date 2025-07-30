# Ensure you're on the branch you want to update with tools
git checkout patch/trial-gallery-support

# Copy gallery tools from gold
git checkout membership-gold -- articles/generate_gallery.py view_gallery.sh
git checkout membership-gold -- generate_rbac_map.py test_rbac_access.py rbac-map.json

# Create the gallery folder if missing
mkdir -p charlotteeverley-site


