import json

with open("gallery-config.json", "r") as f:
    items = json.load(f)

html_start = """<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8' />
  <title>Devon History Gallery</title>
  <script src='https://cdn.tailwindcss.com'></script>
</head>
<body class='bg-gray-100 text-gray-800'>
  <header class='bg-yellow-700 text-white py-6 text-center shadow'>
    <h1 class='text-4xl font-bold'>Devon History Collection</h1>
    <p class='text-sm mt-1'>Faith, Trails, Transit & Family Memories</p>
  </header>
  <main class='max-w-6xl mx-auto px-6 py-10'>
    <div class='grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3'>
"""

html_tiles = ""
for item in items:
    html_tiles += f"""
      <a href="{item['filename']}" class="block bg-white rounded-lg shadow hover:shadow-xl transition overflow-hidden">
        <img src="{item['image']}" alt="{item['title']}" class="w-full h-48 object-cover">
        <div class="p-4">
          <h3 class="text-lg font-semibold text-yellow-800">{item['title']}</h3>
          <p class="text-sm text-gray-600 mt-1">{item['summary']}</p>
        </div>
      </a>
    """


html_end = """
    </div>
  </main>
  <footer class='text-center text-xs text-gray-500 py-6 border-t'>
    (c) 2025 Devon Archive Gallery · Curated by Charlotte Everley Project
  </footer>
</body>
</html>
"""

with open("articles/gallery.html", "w") as f:
    f.write(html_start + html_tiles + html_end)

print("✅ gallery.html generated successfully.")