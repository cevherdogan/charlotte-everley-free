# 🧠 GPT Style-Aware Article Generation – TODO

This document outlines the roadmap for integrating style guide intelligence into Charlotte Everley's AI-driven article generation workflow.

---

## ✅ Immediate Wins

- [x] Document existing visual and editorial styles (`README_STYLE_CODES.md`)
- [x] Classify styles by region or story archetype
- [x] Use style naming convention: `STYLE_GUIDE_<TOPIC>.html`

---

## 🛠️ In Progress

- [ ] Build GPT mode that **detects best matching style** for new article from filename or theme
- [ ] Allow manual override by YAML tag (`style: devon-enhanced`)
- [ ] Inject style-class markers into generated HTML (`<body class="style-devon-enhanced">`)

---

## 🧪 Future Tasks

- [ ] Auto-apply layout blocks from style guides when generating new `.html`
- [ ] Style-aware thumbnail insertion (`devon-home` style = centered poster, `387devonshire` = hero block)
- [ ] Support style preview mode in generator CLI
- [ ] GPT enforcement of editorial tone (serif/sans, formal/informal, length) based on style tag

---

## 🔁 Inputs Needed

- More style guides for `te`, `mainline`, `vfp`
- GPT YAML spec additions for style handling
- HTML generator modules accepting `style_code` as param

---

## 💡 Notes

- All style guides should be registered in `README_STYLE_CODES.md`
- Ideal format for guide ingestion is `.html` or `.md`
- Use `<meta name="style-guide" content="devon-enhanced">` in generated HTML


