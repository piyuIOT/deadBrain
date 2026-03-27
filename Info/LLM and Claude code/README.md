Notes, guides, and prompt templates for LLMs, Claude, and agentic AI tooling.

---

```dataviewjs
const EXCLUDE = new Set(['README', 'CLAUDE']);

const folder = dv.current().file.folder;
const pages  = dv.pages(`"${folder}"`)
    .where(p => !EXCLUDE.has(p.file.name.replace(/\.md$/, '').toUpperCase()))
    .array();

const tree = {};
for (const p of pages) {
    const parts = p.file.path.replace(folder + '/', '').split('/');
    let node = tree;
    for (let i = 0; i < parts.length - 1; i++) {
        node[parts[i]] = node[parts[i]] || {};
        node = node[parts[i]];
    }
    (node._files = node._files || []).push(p);
}

function renderTree(node, depth, path) {
    let md = '';
    const indent = '\t'.repeat(depth);
    for (const p of (node._files || []).sort((a, b) => a.file.name.localeCompare(b.file.name)))
        md += `${indent}- **[[${p.file.path}|${p.file.name.replace(/\.md$/, '')}]]**\n`;
    for (const sf of Object.keys(node).filter(k => k !== '_files').sort()) {
        const sfPath = `${path}/${sf}`;
        const hasReadme = app.vault.getAbstractFileByPath(`${sfPath}/README.md`) !== null;
        const sfLabel = hasReadme ? `**[[${sfPath}/README|${sf}]]**` : `**${sf}**`;
        md += `${indent}- ${sfLabel}\n`;
        md += renderTree(node[sf], depth + 1, sfPath);
    }
    return md;
}

dv.header(1, "INDEX");
dv.paragraph(renderTree(tree, 0, folder));
```
