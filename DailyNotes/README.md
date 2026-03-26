Every day something breaks, something clicks, and most of it quietly disappears into the void if you don't write it down. This is my attempt to not let that happen — a rolling log of what I worked on, what confused me, what I figured out, and what I'm still not sure about. Not polished, not for anyone else, just honest enough to be useful when future me is staring at the same problem again wondering why it looks familiar. If you're reading this, I hope you find something worth stealing.

---

```dataviewjs
const MONTH_NAMES = ['January','February','March','April','May','June',
                     'July','August','September','October','November','December'];
const MONTH_SHORT = ['Jan','Feb','Mar','Apr','May','Jun',
                     'Jul','Aug','Sep','Oct','Nov','Dec'];
const DAY_SHORT   = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];

function extractTasks(content) {
    const lines = content.split('\n');
    let inTasks = false, found = false;
    const tasks = [];
    for (const line of lines) {
        if (line.trim() === '# Tasks') { inTasks = true; found = true; continue; }
        if (inTasks) {
            if (line.startsWith('#') || line.trim() === '---') break;
            const m = line.match(/^-\s+(.+\S)/);
            if (m) tasks.push(m[1]);
        }
    }
    return found ? tasks : null; // null = wrong format
}

const folder = dv.current().file.folder;
const noteMap = {};

for (const p of dv.pages(`"${folder}"`).array()) {
    const rel = p.file.path.replace(folder + '/', '');
    const parts = rel.split('/');
    if (parts.length !== 3) continue;
    const [year, month, dayFile] = parts;
    const day = dayFile.replace('.md', '');
    if (/^\d{4}$/.test(year) && /^\d{2}$/.test(month) && /^\d{2}$/.test(day))
        noteMap[`${year}/${month}/${day}`] = p.file.path;
}

const groupedYM = {};
for (const key of Object.keys(noteMap).sort()) {
    const ym = key.slice(0, 7);
    (groupedYM[ym] = groupedYM[ym] || []).push(parseInt(key.slice(8)));
}

(async () => {
    for (const ym of Object.keys(groupedYM).sort()) {
        const [year, month] = ym.split('/');
        const mi = parseInt(month) - 1, yr = parseInt(year);
        const days = groupedYM[ym].sort((a, b) => a - b);

        dv.header(2, `${MONTH_NAMES[mi]} ${yr}`);

        let md = '';
        for (let d = days[0]; d <= days[days.length - 1]; d++) {
            const ds  = String(d).padStart(2, '0');
            const key = `${year}/${month}/${ds}`;
            const dow = DAY_SHORT[new Date(yr, mi, d).getDay()];
            const label = `${ds} ${MONTH_SHORT[mi]}, ${dow}`;

            if (!noteMap[key]) {
                md += `- **${label}**\n`;
                continue;
            }

            let tasks = null;
            try {
                const tf = app.vault.getAbstractFileByPath(noteMap[key]);
                tasks = extractTasks(await app.vault.read(tf));
            } catch(e) {}

            if (tasks === null) {
                md += `- **${label}**\n`;
            } else if (tasks.length === 0) {
                md += `- **[[${folder}/${key}|${label}]]**\n`;
            } else {
                md += `- **[[${folder}/${key}|${label}]]** — ${tasks.join(' | ')}\n`;
            }
        }
        dv.paragraph(md);
    }
})();
```
