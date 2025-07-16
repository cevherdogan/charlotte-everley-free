# 🖋️ Foundral Community Article Style Guide – Devon Edition

This style guide defines the visual and structural standards for HTML-based community articles like the **Devon Lifestyle Feature** within the Foundral ecosystem.

---

## 🎨 Theme Overview: Devon

A clean, elegant layout that reflects the quiet charm and historic richness of Devon, Pennsylvania.

| Feature        | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| **Fonts**      | - Headings: `Playfair Display` (serif) for elegance  <br> - Body: `Inter` (sans-serif) for clarity |
| **Colors**     | - Accents: `emerald-800`, `emerald-600`, `gray-700`, `gray-800`  <br> - Background: `from-neutral-50 to-emerald-50` (gradient) |
| **Layout**     | - Max-width container `max-w-4xl mx-auto` <br> - Padding: `p-6 md:p-12` <br> - Rounded card sections with `rounded-3xl` and `shadow-2xl` |
| **Icon Styling** | - All icons are SVG-based with `w-6 h-6` and `text-emerald-600` coloring |
| **Headings**   | - `h1`: 5xl, center-aligned, serif <br> - `h2`: xl, emerald tone, flex layout with icon |

---

## 🧱 HTML Base Layout

```html
<body class="bg-gradient-to-br from-neutral-50 to-emerald-50 min-h-screen p-6 md:p-12 text-neutral-800 text-lg leading-relaxed">
  <main class="max-w-4xl mx-auto space-y-10">
    <header class="text-center">
      <h1 class="text-5xl font-semibold text-emerald-900 tracking-tight font-serif">...</h1>
      <p class="mt-2 text-xl text-gray-700 italic">...</p>
    </header>

    <section class="bg-white shadow-2xl rounded-3xl p-8 space-y-8 border-t-4 border-emerald-200">
      <!-- repeatable content blocks -->
    </section>
  </main>
</body>
```

---

## 🔡 Typography

```html
<!-- Import Fonts -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Playfair+Display:wght@600&display=swap" rel="stylesheet" />

<style>
  body {
    font-family: 'Inter', sans-serif;
  }
  h1, h2 {
    font-family: 'Playfair Display', serif;
  }
</style>
```

---

## 🧩 Icon Blocks

Each section begins with a `h2` that uses flex layout and an inline SVG icon:

```html
<h2 class="flex items-center gap-3 text-emerald-800 font-semibold text-xl">
  <svg class="w-6 h-6 text-emerald-600" ... />
  Section Title
</h2>
<p class="mt-1 text-gray-800">Section content goes here...</p>
```

---

## 🔁 Reusability Notes

- Each article (e.g., `devon.html`, `berwyn.html`) follows the same layout.
- Only **content**, **icon**, and **accent tone** may differ to match the spirit of the locale.
- Create a unique visual identity per community while adhering to this baseline.

---

## 📁 File Naming Convention

```
/articles/
├── devon.html
├── berwyn.html
├── haverford.html
```

---

## 🧭 Style Map vs. Other Communities

| Community | Font Family       | Color Base    | Personality Keywords         |
|-----------|-------------------|---------------|------------------------------|
| **Devon**     | Playfair + Inter  | Emerald       | Elegant, serene, artistic    |
| Berwyn    | Georgia (serif)   | Forest + Warm Gray | Cozy, literary, lived-in     |
| Haverford | Coming soon...     | Indigo        | Academic, classic, refined   |

---
