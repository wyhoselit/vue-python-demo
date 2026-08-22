#!/bin/bash
set -e

# Documentation update automation script
# Usage: ./scripts/docs-update.sh "description of changes"

if [ -z "$1" ]; then
    echo "Error: Description of changes required."
    echo "Usage: ./scripts/docs-update.sh \"description of changes\""
    exit 1
fi

DESCRIPTION=$1
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date +%s)
BRANCH_NAME="docs/update-$TIMESTAMP"

echo "=== Updating master branch ==="
git checkout master
git pull origin master

echo "=== Creating documentation branch: $BRANCH_NAME ==="
git checkout -b "$BRANCH_NAME"

echo "=== Regenerating OpenAPI specification ==="
cd backend
PYTHONPATH=. uv run python scripts/update_openapi.py

echo "=== Validating documentation build ==="
uv run mkdocs build --strict
cd ..

echo "=== Creating changelog entry ==="
CHANGELOG_DIR="docs/changelog"
mkdir -p "$CHANGELOG_DIR"
echo "- $DATE: $DESCRIPTION" >> "$CHANGELOG_DIR/updates.md"

echo "=== Committing and pushing changes ==="
git add .
git commit -m "docs: $DESCRIPTION"
git push origin "$BRANCH_NAME"

echo "=== Creating GitHub Pull Request ==="
gh pr create --title "docs: $DESCRIPTION" --body "Automated documentation update: $DESCRIPTION" --base master --head "$BRANCH_NAME"

echo "=== Successfully started documentation update process ==="
