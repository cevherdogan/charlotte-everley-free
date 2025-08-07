import yaml
import json

GALLERY_YAML = "config/gallery_items.yaml"
ACCESS_JSON = "access_map.json"
OUTPUT_HTML = "charlotteeverley-site/gallery.generated.html"

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Gallery – RBAC View</title>
  <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet" />
  <style>.tile {{ position: relative; }}</style>
</head>
<body class="bg-gray-50 p-6 font-serif">
  <div class="mb-6">
    <label for="planSelector" class="text-sm font-semibold">Plan seçin:</label>
    <select id="planSelector" class="ml-2 border rounded px-2 py-1 text-sm">
      <option value="all">Tümü</option>
      <option value="free">Free</option>
      <option value="bronze">Bronze</option>
      <option value="silver">Silver</option>
      <option value="premier">Premier</option>
    </select>
  </div>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
{tiles}
  </div>
  <script>
    const selector = document.getElementById("planSelector");
    selector.addEventListener("change", () => {{
      const tier = selector.value;
      document.querySelectorAll(".tile").forEach(tile => {{
        tile.style.display = (tier === "all" || tile.dataset.tier === tier) ? "" : "none";
      }});
    }});
  </script>
</body>
</html>"""

def build_tile_html(item):
    badge = f'<span class="absolute top-0 left-0 bg-gray-800 text-white text-xs px-2 py-1 rounded-br">{{item["tier"].capitalize()}}</span>' if item.get("plan_badge") else ""
    return f'''
    <div class="tile border rounded shadow p-4 bg-white" data-tier="{{item["tier"]}}">
      {{badge}}
      <img src="{{item["image"]}}" alt="{{item["title"]}}" class="w-full h-40 object-cover rounded mb-2" />
      <h3 class="text-lg font-semibold">{{item["title"]}}</h3>
      <p class="text-sm text-gray-600">{{item["description"]}}</p>
      <p class="text-xs italic text-gray-400">{{item.get("upgrade_hint", "")}}</p>
      <a href="/membership/{{item["tier"]}}/articles/{{item["slug"]}}.html" class="inline-block mt-2 text-blue-600 text-sm underline">{{item["cta"]}}</a>
    </div>
    '''

def main():
    with open(GALLERY_YAML, "r") as f:
        gallery = yaml.safe_load(f)

    tiles_html = "\n".join([build_tile_html(item) for item in gallery])
    final_html = TEMPLATE.format(tiles=tiles_html)

    with open(OUTPUT_HTML, "w") as out:
        out.write(final_html)
        print(f"✅ HTML galeri dosyası oluşturuldu: {OUTPUT_HTML}")

if __name__ == "__main__":
    main()
