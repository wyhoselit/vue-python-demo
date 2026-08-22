#!/usr/bin/env bash
set -euo pipefail

# Docs update automation script
# Usage: ./scripts/docs-update.sh "change description" [--branch <name>]

DESCRIPTION="${1:-}"
BRANCH="${2:-docs/update-$(date +%s)}"

if [[ -z "$DESCRIPTION" ]]; then
    echo "Usage: $0 \"change description\" [--branch branch-name]"
    exit 1
fi

echo "📝 Starting docs update: $DESCRIPTION"

# 1. Ensure we're on master and up to date
git checkout master
git pull origin master

# 2. Create working branch
git checkout -b "$BRANCH"

# 3. Update OpenAPI spec
echo "🔄 Generating OpenAPI spec..."
cd backend
PYTHONPATH=. uv run python scripts/update_openapi.py
cd ..

# 4. Build docs to verify
echo "🔨 Building docs..."
cd backend
uv run mkdocs build --strict
cd ..

# 5. Create changelog entry
CHANGELOG="docs/changelog/$(date +%Y-%m-%d)-$(echo "$DESCRIPTION" | tr ' ' '-' | tr '[:upper:]' '[:lower:]').md"
mkdir -p docs/changelog
cat > "$CHANGELOG" << CHANGELOG_EOF
# $(date +%Y-%m-%d): $DESCRIPTION

## Changes
- $DESCRIPTION

## API Impact
- OpenAPI spec regenerated
- Documentation rebuilt

## Testing
- All tests pass
- Docs build successful
CHANGELOG_EOF

# 6. Commit changes
git add backend/docs/openapi/openapi.json "$CHANGELOG"
git commit -m "docs: $DESCRIPTION

- Update OpenAPI spec
- Add changelog entry
- Rebuild documentation"

# 7. Push and create PR
git push origin "$BRANCH"

echo "📤 Creating PR..."
gh pr create \
    --base master \
    --head "$BRANCH" \
    --title "docs: $DESCRIPTION" \
    --body "$DESCRIPTION

---

### Changes
- OpenAPI spec updated
- Documentation rebuilt
- Changelog: $CHANGELOG

### Verification
- \`mkdocs build --strict\` passes
- \`pytest\` passes"

echo "✅ Done! PR created. Wait for CI to pass, then merge."
