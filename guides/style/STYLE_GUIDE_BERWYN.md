# 🖋️ Foundral Community Article Style Guide – Berwyn Edition

This guide outlines the visual style and structure of the **Berwyn Community** article, emphasizing warm tradition, neighborly charm, and a nature-forward aesthetic. It builds on the Foundral layout base while introducing its own tone and flair.

---

## 🎨 Theme Overview: Berwyn

A heartfelt and cozy layout that reflects the “lived-in grace” and artistic, connected atmosphere of Berwyn, PA.

| Feature        | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| **Fonts**      | - Headings and body: `'Georgia', serif` for literary warmth and familiarity |
| **Colors**     | - Text: `#2c2c2c` (warm neutral) <br> - Accents: forest green `#14532d`, lime `#10b981` |
| **Layout**     | - Max-width: `900px` centered block <br> - Margin/padding: `2rem auto`, `2rem` |
| **Highlights** | - Quote blocks styled with `#ecfdf5` background, `#10b981` left-border, and italic text |
| **Images**     | - Soft rounded corners, subtle drop shadow, full width responsiveness |

---

## 🧱 HTML Layout Skeleton

```html
<body style="background:#f9f9f7; max-width:900px; margin:2rem auto; padding:2rem;">
  <h1 style="color:#14532d;">...</h1>

  <p class="highlight">...</p>

  <h2 style="color:#166534;">...</h2>
  <p>...</p>

  <img src="..." alt="..." />

  <p class="highlight">...</p>
</body>
```

---

## 🔡 Typography

```css
body {
  font-family: 'Georgia', serif;
  line-height: 1.7;
  color: #2c2c2c;
}
h1 {
  font-size: 2.25rem;
  color: #14532d;
}
h2 {
  font-size: 1.5rem;
  color: #166534;
}
```

---

## ✨ Highlight Block Style

```css
.highlight {
  background: #ecfdf5;
  padding: 0.5rem 1rem;
  border-left: 4px solid #10b981;
  margin: 1.5rem 0;
  font-style: italic;
}
```

Use for:
- Pull quotes
- Emotional tones
- Cultural anchors

---

## 🖼️ Image Guidelines

```css
img {
  max-width: 100%;
  border-radius: 10px;
  margin: 1.5rem 0;
  box-shadow: 0 6px 14px rgba(0, 0, 0, 0.1);
}
```

- Place midway or end of article
- Recommended alt text: `"Illustration of Berwyn Community"`

---

## 🧭 Content Rhythm

| Section Title               | Emoji/Icon | Content Style                             |
|----------------------------|------------|-------------------------------------------|
| Morning Rituals            | 🌄         | Warm, neighborly, food + welcome          |
| Real Homes, Real Community | 🏘️         | Architecture + social flow                |
| Green Spaces               | 🌳         | Nature, wellness, trails                  |
| The Town That Shows Up     | 🎭         | Culture, unity, local support             |

---

## 🔁 Reusability Notes

- Berwyn is a **serif-forward**, **cozy**, **intimate** style.
- Emphasize “lived-in” tone, with less geometry and more *organic* text flow.
- Use highlight blocks more liberally for tone-setting transitions.

---

## 🧭 Style Map vs. Other Communities

| Community | Font Family       | Color Base    | Personality Keywords         |
|-----------|-------------------|---------------|------------------------------|
| Devon     | Playfair + Inter  | Emerald       | Elegant, serene, artistic    |
| **Berwyn**    | Georgia (serif)   | Forest + Warm Gray | Cozy, literary, lived-in     |
| Haverford | Coming soon...     | Indigo        | Academic, classic, refined   |

---
