# Converting Presenterm slides to Marp → PPTX (16:10)

Reference for converting this project's Presenterm markdown deck
(`apptainer_hpc_workshop.md`) to a properly formatted PowerPoint file at
16:10 aspect ratio, via [Marp](https://marp.app/).

Presenterm's own PPTX export discards formatting (plain text dump). Pandoc
works but needs a hand-built reference template. Marp is the closest match
to Presenterm's authoring model and has native 16:10 PPTX export.

---

## Prerequisites

```bash
brew install marp-cli       # installs the `marp` binary
```

That's it — no Node project, no config files needed.

---

## Workflow

1. **Copy** the Presenterm source to a Marp-specific file so the original
   stays untouched:
   ```bash
   cp apptainer_hpc_workshop.md apptainer_hpc_workshop_marp.md
   ```
2. **Rewrite** the Presenterm-specific directives (see mapping table below).
3. **Build** the PPTX:
   ```bash
   marp --pptx apptainer_hpc_workshop_marp.md \
        -o apptainer_hpc_workshop_marp.pptx \
        --allow-local-files
   ```
   `--allow-local-files` is required whenever the deck references images
   on disk (e.g. `img/all.jpeg`).

Optional extras:
- `--pdf` — same source → 16:10 PDF
- `--html` — self-contained HTML deck for browser viewing
- `--theme path/to/custom.css` — external theme instead of inline `style:`

---

## Directive mapping: Presenterm → Marp

| Presenterm                                       | Marp equivalent                                                         |
|--------------------------------------------------|-------------------------------------------------------------------------|
| Front-matter `theme: { name: tokyonight-night }` | Front-matter `theme: default` + `class: invert` + inline `style:` block |
| `<!-- end_slide -->`                             | `---` on its own line                                                   |
| `<!-- pause -->`                                 | **Removed** — Marp PPTX has no step-reveal; add animations in PowerPoint if needed |
| `<!-- column_layout: [1,1] -->` + `<!-- column: N -->` + `<!-- reset_layout -->` | `<div class="columns">` / `<div>…</div>` blocks with CSS grid |
| `<!-- speaker_note: \| … -->` (YAML-style HTML comment) | Plain `<!-- … -->` HTML comment — Marp promotes these to PowerPoint presenter notes automatically |
| `<!-- new_line -->`                              | Blank line                                                              |
| `<!-- alignment: center -->` / `<!-- jump_to_middle -->` | Per-slide class, e.g. `<!-- _class: title-slide -->` with centering CSS |
| `<!-- incremental_lists: true -->`               | Removed                                                                 |
| `![image:width:100%](path)`                      | `![w:100%](path)` (Marp sizing syntax: `w:`, `h:`, `bg`, etc.)          |
| Code fence info strings like ` ```bash +exec `, ` +line_numbers ` | Strip extras — keep just ` ```bash `                                    |
| Setext heading `Title\n===`                      | ATX heading `# Title` (works either way, but ATX is cleaner)            |
| Inline `<span style="color: #...">…</span>`      | Works as-is, or replace with CSS utility class like `<span class="accent">` |

---

## Marp front matter used for this deck

```yaml
---
marp: true
size: 16:10
paginate: true
theme: default
class: invert
title: "Containers for HPC"
author: "HPC Research Computing Workshop"
style: |
  section { background-color: #1a1b26; color: #c0caf5; font-size: 26px; }
  section h1, section h2, section h3 { color: #7aa2f7; }
  section strong { color: #e0af68; }
  section blockquote {
    border-left: 4px solid #bb9af7;
    background: #24283b;
    padding: 0.6em 1em;
  }
  section pre {
    background: #16161e;
    border: 1px solid #414868;
    font-size: 18px;
  }
  .columns { display: grid; grid-template-columns: 1fr 1fr; gap: 1.2rem; }
  .cols3   { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; }
  .cols4   { display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 0.8rem; }
  .accent  { color: #7dcfff; font-weight: 600; }
  .warn    { color: #f59e0b; font-weight: 600; }
  section.title-slide { justify-content: center; text-align: center; }
---
```

Colors approximate the Tokyonight-night scheme used in Presenterm. Adjust
`section { font-size: }` if content overflows — 24–28px is the usable range
for 16:10 at Marp's default slide resolution.

---

## Column layout pattern

```markdown
<div class="columns">
<div>

Left column content — **blank lines around the inner `<div>` tags are
required** so Marp parses the markdown inside them.

</div>
<div>

Right column content.

</div>
</div>
```

Same pattern with `cols3` / `cols4` classes for 3- and 4-up layouts.

---

## Speaker notes

Any HTML comment on a slide becomes presenter notes in the exported PPTX.
Strip the Presenterm `speaker_note: |` YAML prefix — just leave the text:

```markdown
<!--
This is now a plain comment. PowerPoint will show it as presenter notes
under the slide in Presenter View.
-->
```

---

## Title / section-divider slides

Use a per-slide class to center content:

```markdown
---

<!-- _class: title-slide -->

# HANDS-ON DEMOS

---
```

The `.title-slide` class is defined in the inline `style:` block with
`justify-content: center; text-align: center;`.

---

## Known limitations

- **No step reveals.** Marp doesn't translate `<!-- pause -->`-style
  incremental reveals into PPTX animations. All bullets on a slide appear
  at once. If you need click-by-click reveal, add animations in PowerPoint
  after export, or split into multiple slides.
- **PPTX is rendered via headless Chromium**, so slides are composed of
  editable text boxes + images, not a single raster image. Most CSS carries
  through, but complex pseudo-selectors or gradients may not.
- **Font size** is bound by the slide box; long code blocks can overflow.
  Lower the `section pre { font-size: }` rule or split the slide.
- **Emojis** render via the OS emoji font at export time. Color emojis
  should work; if they render as squares, install a system emoji font or
  replace with text.

---

## Rebuild command (quick reference)

```bash
cd /Users/acchapm1/ASU/presentations/hpc-containers-slides

marp --pptx apptainer_hpc_workshop_marp.md \
     -o apptainer_hpc_workshop_marp.pptx \
     --allow-local-files

# Same source, other formats:
marp --pdf  apptainer_hpc_workshop_marp.md -o deck.pdf  --allow-local-files
marp --html apptainer_hpc_workshop_marp.md -o deck.html --allow-local-files

# Live preview while editing:
marp --server .
# → open http://localhost:8080 and click the deck
```

---

## When to reach for a different tool

- **Need pixel-perfect match to the existing PDF, not editability:** convert
  the PDF to PPTX with Acrobat Pro or `pdf2pptx`. Each slide becomes an
  embedded image — not editable, but visually identical.
- **Need Pandoc-style control / citations / cross-refs:** use Quarto with
  `format: pptx` and a 16:10 `reference-doc` template.
- **Want click-by-click reveals preserved:** keep using Presenterm for
  presenting, and use Marp/Pandoc only for the handout PPTX.
