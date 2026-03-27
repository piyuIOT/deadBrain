# Output Rules
- No introductions, summaries, or filler text. Start with content directly.
- Rich use of obsidian markdown features:
	- Use tables for structured data (pin mappings, signal specs, comparisons).
	- Use mermaid diagrams for system/signal flow — keep nodes labeled with part numbers, group by functional blocks.
	- Use mathjax for formula and equations, inline mathjax for smaller formulas.
	- Use callouts for important things that need dedicated attention: non-obvious pin behaviour, non-obvious code structure, critical hardware/firmware/software info.
- Use headers to separate functional sections, not paragraphs of explanation.
- Include exact part numbers, protocol names, and pin assignments. No vague descriptions.
- Don't explain what's obvious from context. Only annotate where behaviour is non-obvious.
- Do not use /n in mermaid diagrams, it is not supported

---
# Vault Organization
## Folder Structure
- Top-level folders: `Hardware/`, `Software/`, `Info/`, `Personel/`
- Subfolder depth: max 2 levels below top-level (e.g. `Hardware/Audio recorder/`)
- Each major folder has a `README.md` acting as its section index
- Root `README.md` is the master index — lists all sections and key files with relative links
- Assets go in `assets/<note-name>/` adjacent to the note that uses them
## Linking
- Use relative markdown links, not Obsidian wikilinks
- Encode spaces as `%20` in link paths: `[Git doc](Info/Git/Git%20doc.md)`
- Cross-reference related notes explicitly in a `# Resources` section at the top
- External resources (datasheets, wikis, schematics) also go in `# Resources`
## Daily Notes
- Location: `DailyNotes/YYYY/MM/DD.md`
- Index: `DailyNotes/README.md` — dataviewjs, auto-reads all notes, do not edit manually
- Template: `DailyNotes/template.md`
- Scripts: `DailyNotes/create_notes.sh` (create blank notes for a date range), `DailyNotes/fill_tasks.py` (backfill tasks from Work.md)
- One note per working day; weekends included if work was done
- Note structure (in order, no frontmatter):
  1. `# Misc` — scratchpad, anything
  2. `# Tasks` — what was done
  3. `# Issues & Observations` — bugs, anomalies
  4. `# Notes` — knowledge, reasoning, learnings; use sub-headers freely
  5. `# Conclusion` — single blockquote, key takeaway
- Work.md one-liners are the source of truth for task entries in old notes