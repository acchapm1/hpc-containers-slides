
# Running it

```bash
# Dev mode — auto-reloads on save (great for editing)
presenterm apptainer_hpc_workshop.md

# Present mode — clean, no reload indicator
presenterm --present apptainer_hpc_workshop.md

# Speaker notes in a second terminal window
presenterm apptainer_hpc_workshop.md --publish-speaker-notes
# (second terminal)
presenterm apptainer_hpc_workshop.md --listen-speaker-notes
```

---

## What was converted and how

**Structure** — Each PPTX slide became a `<!-- end_slide -->` delimited section with a setext-style (`===`) slide title, which presenterm renders with special title styling.

**Speaker notes** — Every single speaker note from the PPTX was preserved using `<!-- speaker_note: ... -->` blocks, so they work with presenterm's two-window speaker notes mode.

**Two-column layouts** — PPTX side-by-side panels (like Definition Files, Demo code+commands) were converted to `<!-- column_layout: [1, 1] -->` with `<!-- column: 0/1 -->` and `<!-- reset_layout -->`.

**Code blocks** — All code blocks use proper language tags (`bash`, `python`) for syntax highlighting. Demo 1's pull command is marked `+exec` so you can press `Ctrl+E` to actually run it live on screen.

**Incremental reveals** — The Key Takeaways slide uses `<!-- incremental_lists: true -->` so bullet points appear one at a time as you advance.

**Separator slides** — The "HANDS-ON DEMOS" and "Key Takeaways & Resources" transition slides use `<!-- jump_to_middle -->` to center the title dramatically on screen.

**Theme** — Set to `dark` with the ocean blue accent color (`#00b4d8`) from the original PPTX, with `base16-ocean.dark` code highlighting and a progress bar footer.
