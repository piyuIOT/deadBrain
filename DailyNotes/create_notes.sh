#!/usr/bin/env bash
# Creates daily notes for all working days logged in Work.md
# Skips weekends, does not overwrite existing notes

VAULT_ROOT="$(dirname "$0")"

TEMPLATE="# Misc
-

---

# Tasks
-

---

# Issues & Observations
-

---

# Notes

---

# Conclusion
>
"

# All working days from Work.md (skip weekends and leaves — those still get a note)
# Range: 2026-02-02 to 2026-03-26, skip SAT/SUN

start="2026-02-02"
end="2026-03-26"

current="$start"
created=0
skipped=0

while [[ "$current" < "$end" || "$current" == "$end" ]]; do
    year="${current:0:4}"
    month="${current:5:2}"
    day="${current:8:2}"
    dir="$VAULT_ROOT/$year/$month"
    file="$dir/$day.md"
    mkdir -p "$dir"
    if [[ ! -f "$file" ]]; then
        echo "$TEMPLATE" > "$file"
        echo "Created: $file"
        ((created++))
    else
        echo "Exists:  $file"
        ((skipped++))
    fi
    # Advance by 1 day
    current=$(date -j -f "%Y-%m-%d" -v+1d "$current" "+%Y-%m-%d" 2>/dev/null || date -d "$current + 1 day" "+%Y-%m-%d")
done

echo ""
echo "Done — created: $created, skipped (already exist): $skipped"
