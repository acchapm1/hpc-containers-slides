# Presenterm

---

## The Pick: `presenterm`

**Install:** `brew install presenterm` (macOS) or `cargo install presenterm`
**Docs:** `mfontanini.github.io/presenterm`
**Repo:** `github.com/mfontanini/presenterm`

---

### Why presenterm wins over every alternative

**vs. `slides` (charmbracelet/maaslalani)**
`slides` is the other strong terminal contender — it's elegant and Go-based. But it stalled in active development and its code execution is basic (press `Ctrl+E`, runs the block, dumps output). Presenterm explicitly lists Ghostty as a supported terminal for images and animated GIFs, while `slides` does not. For an HPC demo, presenterm's richer feature set wins.

**vs. `patat`**
Patat is feature-rich and uses Pandoc under the hood, supports code evaluation, speaker notes in a second window, and auto-reload — genuinely solid. But it requires Haskell tooling, has a smaller community, and its code execution is more limited.

**vs. `mdp`**
mdp is a command-line tool for making presentations from markdown files supporting lists, images, headers, and code blocks — but it's essentially unmaintained and cannot execute code on a slide. A non-starter for your use case.

---

### What makes presenterm the strongest choice

**1. Actively maintained with dedicated documentation site**
Presenterm has a full documentation site at mfontanini.github.io/presenterm — not just a README. It covers installation, theming, code execution, speaker notes, and PDF export in separate organized pages.

**2. Code execution built in — the right way**
The code execution system in presenterm provides the ability to execute code snippets within presentations and display their results directly in the terminal, enabling interactive demonstrations, live code execution, and even the generation of images from code during presentations. For your Apptainer demo, this means you can have a bash block on slide that actually runs `apptainer exec ...` and shows the output live.

**3. Ghostty is explicitly supported**
Images and animated GIFs work on terminals like kitty, iterm2, wezterm, Ghostty, and foot. You're not on a workaround — Ghostty is a first-class supported terminal.

**4. Feature set built for technical talks**
Presenterm supports selective/dynamic code highlighting that only highlights portions of code at a time, column layouts, LaTeX and typst formula rendering, snippet execution for various programming languages including execution inside pseudo terminals, export to PDF and HTML, slide transitions, pausing portions of slides, custom key bindings, and automatic reload every time the file changes.

**5. Community adoption at real conferences**
Users who have adopted presenterm for work presentations highlight the fluid workflow between presentation content and terminal-based development environments — being able to seamlessly transition from slides to example code is really nice, with no need to juggle multiple windows, just terminal tabs or even `ctrl+z`/`fg`. This is exactly what you want when flipping between your slides and a live `apptainer shell` demo.

---

### Quick-start for your Apptainer talk

```bash
# Install
brew install presenterm        # macOS
# or
cargo install presenterm

# Run your presentation
presenterm apptainer_talk.md

# Auto-reload while editing (dev mode)
presenterm apptainer_talk.md   # saves auto-reload

# Present mode (disables reload, cleaner)
presenterm --present apptainer_talk.md
```

A slide with live code execution looks like this in the `.md` file:

````markdown
<!-- end_slide -->

## Demo: Check container Python version

```bash +exec
apptainer exec python311.sif python3 --version
```
````

Press `Ctrl+E` on that slide and the command runs live, output appears below the code block — right there in Ghostty, never leaving the terminal.
