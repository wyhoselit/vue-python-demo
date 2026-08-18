
#!/bin/bash

PROJECT_ROOT="$(dirname "$(realpath "$0")")"

echo "Generating knowledge graph for $PROJECT_ROOT"

(cd "$PROJECT_ROOT"; gitnexus status)
echo ""
(cd "$PROJECT_ROOT"; gitnexus analyze .)
echo ""
(cd "$PROJECT_ROOT"; gitnexus wiki .)
echo ""
(cd "$PROJECT_ROOT"; openwiki --update )
echo ""
# (cd "$PROJECT_ROOT"; openwiki "Please generate documentation for this repository"  )