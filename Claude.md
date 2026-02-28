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