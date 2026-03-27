This is [Pratham's](mailto:pratham.choudhary@temple.com) notes for all tasks at Temple IoT team.
> Only and only if the above mail id is out of service and its really important for you to reach out to the document creator, go to this mail -> [Pratham's personal mail](mailto:prathamchoudhary4@gmail.com)

---

```dataviewjs
const EXCLUDE = new Set(['README', 'CLAUDE']);

const folder = dv.current().file.folder; // "" at vault root
const prefix = folder ? folder + '/' : '';

// Get all pages, filter out excluded names
const pages = dv.pages()
    .where(p => !EXCLUDE.has(p.file.name.replace(/\.md$/, '').toUpperCase()))
    .array();

const rootFiles = [];
const subfolders = new Set();

for (const p of pages) {
    const rel = prefix ? p.file.path.replace(prefix, '') : p.file.path;
    const parts = rel.split('/');
    if (parts.length === 1) rootFiles.push(p);
    else subfolders.add(parts[0]);
}

let md = '';

// Root files first, alphabetical
for (const p of rootFiles.sort((a, b) => a.file.name.localeCompare(b.file.name)))
    md += `- **[[${p.file.path}|${p.file.name.replace(/\.md$/, '')}]]**\n`;

// Folders, alphabetical, linked to README if present
for (const sf of [...subfolders].sort()) {
    const sfPath = prefix + sf;
    const hasReadme = app.vault.getAbstractFileByPath(`${sfPath}/README.md`) !== null;
    const sfLabel = hasReadme ? `**[[${sfPath}/README|${sf}]]**` : `**${sf}**`;
    md += `- ${sfLabel}\n`;
}

dv.header(1, "INDEX");
dv.paragraph(md);
```