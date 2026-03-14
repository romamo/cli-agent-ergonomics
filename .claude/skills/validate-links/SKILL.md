---
name: validate-links
description: Validate all cross-links in the CLI Agent Ergonomics specification — broken file links, missing schema sections, and schema↔requirement symmetry. Use when files have been added or edited, or to check the project is internally consistent.
tools: Bash
---

# Validate Cross-Links

Run the scripts below in order. Report every failure found. If all checks pass, confirm with a summary of what was checked and how many links were verified.

Each script detects the project root via `git rev-parse --show-toplevel`, falling back to the current directory if not in a git repo.

---

## Script 1 — Broken file links in all markdown files

Extracts every relative link from every `.md` file and checks the target exists.

```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd) && cd "$ROOT" && ERRORS=0
while IFS= read -r mdfile; do
  while IFS= read -r link; do
    target="$(dirname "$mdfile")/$link"
    resolved=$(python3 -c "import os,sys; print(os.path.normpath(sys.argv[1]))" "$target")
    if [ ! -e "$resolved" ]; then
      echo "BROKEN: $mdfile -> $link"
      ERRORS=$((ERRORS + 1))
    fi
  done < <(perl -ne 'while (/\[[^\]]*\]\(([^)#]+)\)/g) { print "$1\n" }' "$mdfile" \
           | grep -v '^http' | grep -v '^mailto')
done < <(find "$ROOT" -name "*.md" \
           -not -path "*/.git/*" \
           -not -path "*/node_modules/*" \
           -not -path "*/.claude/plugins/*")
echo "---"
echo "Broken links: $ERRORS"
```

---

## Script 2 — Schema ↔ requirement symmetry

**Direction 1:** For each schema `.md` "Used by" requirement → that requirement must have a `## Schema` link back to this schema's `.json`.

**Direction 2:** For each requirement's `## Schema` link → that schema's `.md` "Used by" must include this requirement.

```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd) && cd "$ROOT" && ERRORS=0

echo "=== Direction 1: Schema 'Used by' -> Requirement '## Schema' ==="
for schema_md in "$ROOT"/schemas/*.md; do
  base=$(basename "$schema_md")
  [[ "$base" == "index.md" || "$base" == "codegen-guide.md" ]] && continue
  schema_json="${base%.md}.json"

  while IFS= read -r req_id; do
    tier=$(echo "$req_id" | perl -ne '/REQ-([A-Z])-\d+/ && print lc($1)')
    num=$(echo "$req_id"  | perl -ne '/REQ-[A-Z]-(\d+)/ && print $1+0')
    req_file=$(find "$ROOT/requirements" -name "${tier}-$(printf '%03d' $num)-*.md" 2>/dev/null | head -1)

    if [ -z "$req_file" ]; then
      echo "MISSING FILE: $base says 'Used by $req_id' but no matching file in requirements/"
      ERRORS=$((ERRORS + 1))
      continue
    fi
    if ! grep -q "$schema_json" "$req_file"; then
      echo "MISSING BACK-LINK: $req_id has no link to $schema_json  (schema: $base)"
      ERRORS=$((ERRORS + 1))
    fi
  done < <(perl -ne 'while (/(REQ-[A-Z]-\d+)/g) { print "$1\n" }' "$schema_md" \
             | grep "Used by" 2>/dev/null || \
           grep "Used by" "$schema_md" \
             | perl -ne 'while (/(REQ-[A-Z]-\d+)/g) { print "$1\n" }')
done

echo ""
echo "=== Direction 2: Requirement '## Schema' -> Schema 'Used by' ==="
for req_file in "$ROOT"/requirements/[fco]-*.md; do
  req_id=$(grep -m1 "REQ-[A-Z]-[0-9]" "$req_file" \
           | perl -ne '/(REQ-[A-Z]-\d+)/ && print $1')
  [ -z "$req_id" ] && continue

  # Extract content of ## Schema section only
  schema_section=$(awk '/^## Schema/{found=1; next} /^## /{found=0} found{print}' "$req_file")
  [ -z "$schema_section" ] && continue

  while IFS= read -r schema_json; do
    schema_md="$ROOT/schemas/${schema_json%.json}.md"
    if [ ! -f "$schema_md" ]; then
      echo "MISSING SCHEMA FILE: $req_id links to $schema_json but schemas/${schema_json%.json}.md not found"
      ERRORS=$((ERRORS + 1))
      continue
    fi
    if ! grep -q "$req_id" "$schema_md"; then
      echo "MISSING BACK-LINK: $schema_json 'Used by' does not include $req_id"
      ERRORS=$((ERRORS + 1))
    fi
  done < <(echo "$schema_section" | perl -ne 'while (/\b([\w-]+\.json)\b/g) { print "$1\n" }')
done

echo "---"
echo "Symmetry errors: $ERRORS"
```

---

## Script 3 — Index completeness

Every file listed in `requirements/index.md` and `schemas/index.md` must exist, and every file in those directories must be listed.

```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd) && cd "$ROOT" && ERRORS=0

echo "=== requirements/index.md ==="

# Every .md linked from index must exist
while IFS= read -r fname; do
  [ -f "$ROOT/requirements/$fname" ] || {
    echo "MISSING: index links to $fname but file not found"
    ERRORS=$((ERRORS + 1))
  }
done < <(perl -ne 'while (/\(([\w-]+\.md)\)/g) { print "$1\n" }' \
           "$ROOT/requirements/index.md")

# Every requirement file must appear in index
for req_file in "$ROOT"/requirements/[fco]-*.md; do
  fname=$(basename "$req_file")
  grep -q "$fname" "$ROOT/requirements/index.md" || {
    echo "UNLISTED: $fname not in requirements/index.md"
    ERRORS=$((ERRORS + 1))
  }
done

echo ""
echo "=== schemas/index.md ==="

# Every .json linked from index must exist
while IFS= read -r fname; do
  [ -f "$ROOT/schemas/$fname" ] || {
    echo "MISSING: index links to $fname but file not found"
    ERRORS=$((ERRORS + 1))
  }
done < <(perl -ne 'while (/\(([\w-]+\.json)\)/g) { print "$1\n" }' \
           "$ROOT/schemas/index.md")

# Every schema .json must appear in index
for schema_file in "$ROOT"/schemas/*.json; do
  fname=$(basename "$schema_file")
  grep -q "$fname" "$ROOT/schemas/index.md" || {
    echo "UNLISTED: $fname not in schemas/index.md"
    ERRORS=$((ERRORS + 1))
  }
done

echo "---"
echo "Index errors: $ERRORS"
```

---

## Output format

After all three scripts, report:

```
## Link validation results

### Broken file links      — N errors
### Schema ↔ req symmetry  — N errors
### Index completeness     — N errors

Total: N errors
```

List every error with the file it came from. For each error suggest the fix:
- `BROKEN` → update the link or create the missing file
- `MISSING BACK-LINK` → add `## Schema` to the requirement or add the requirement to schema "Used by"
- `MISSING FILE` → create the file or remove the stale reference
- `UNLISTED` → add a row to the index
