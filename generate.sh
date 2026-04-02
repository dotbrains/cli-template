#!/usr/bin/env bash
set -euo pipefail
export LC_ALL=C

# ─── CLI Template Generator ───────────────────────────────────────────────────
# Scaffolds a new CLI project from the monorepo template.
#
# Usage:
#   ./generate.sh --lang <go|python|rust|typescript> --name <project-name> \
#     --desc "<one-line>" --desc-long "<longer>" [--output <dir>]
#
# Example:
#   ./generate.sh --lang go --name prr --desc "AI PR reviewer" \
#     --desc-long "Run AI-powered code reviews on GitHub pull requests."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LANGUAGES_DIR="$SCRIPT_DIR/languages"
SHARED_DIR="$SCRIPT_DIR/shared"
TEMPLATES_DIR="$SCRIPT_DIR/templates"

# ─── Defaults ──────────────────────────────────────────────────────────────────
LANG=""
NAME=""
DESC=""
DESC_LONG=""
OUTPUT=""

# ─── Parse Arguments ───────────────────────────────────────────────────────────
usage() {
    cat <<EOF
Usage: $(basename "$0") --lang <go|python|rust|typescript> --name <name> --desc "<desc>" --desc-long "<long desc>" [--output <dir>]

Options:
  --lang        Language: go, python, rust, or typescript
  --name        Project name (lowercase, hyphen-separated)
  --desc        One-line description
  --desc-long   Longer description (1-2 sentences)
  --output      Output directory (default: output/<name>)
  -h, --help    Show this help
EOF
    exit 1
}

while [[ $# -gt 0 ]]; do
    case $1 in
        --lang)      LANG="$2"; shift 2 ;;
        --name)      NAME="$2"; shift 2 ;;
        --desc)      DESC="$2"; shift 2 ;;
        --desc-long) DESC_LONG="$2"; shift 2 ;;
        --output)    OUTPUT="$2"; shift 2 ;;
        -h|--help)   usage ;;
        *)           echo "Unknown option: $1"; usage ;;
    esac
done

# ─── Validate ──────────────────────────────────────────────────────────────────
[[ -z "$LANG" ]] && echo "Error: --lang is required (go, python, rust, or typescript)" && exit 1
[[ -z "$NAME" ]] && echo "Error: --name is required" && exit 1
[[ -z "$DESC" ]] && echo "Error: --desc is required" && exit 1
[[ -z "$DESC_LONG" ]] && echo "Error: --desc-long is required" && exit 1

if [[ "$LANG" != "go" && "$LANG" != "python" && "$LANG" != "rust" && "$LANG" != "typescript" ]]; then
    echo "Error: --lang must be go, python, rust, or typescript (got: $LANG)"
    exit 1
fi

LANG_DIR="$LANGUAGES_DIR/$LANG"
if [[ ! -d "$LANG_DIR" ]]; then
    echo "Error: language directory not found: $LANG_DIR"
    exit 1
fi

OUTPUT="${OUTPUT:-output/$NAME}"
if [[ -d "$OUTPUT" ]]; then
    echo "Error: output directory already exists: $OUTPUT"
    exit 1
fi

# ─── Helper: Recursively copy, skip hidden dirs and specific patterns ──────────
copy_tree() {
    local src="$1"
    local dst="$2"
    mkdir -p "$dst"
    rsync -a --exclude='.git' --exclude='.github' "$src/" "$dst/"
}

# ─── Helper: Render template with language blocks ──────────────────────────────
# Template syntax:
#   {{#go}}...{{/go}}       — included only when lang=go
#   {{#python}}...{{/python}} — included only when lang=python
#   {{#rust}}...{{/rust}}   — included only when lang=rust
#   {{#typescript}}...{{/typescript}} — included only when lang=typescript
#
# The render process:
#   1. Extract content of the chosen language's blocks
#   2. Strip remaining {{#lang}}...{{/lang}} markers (for other languages)
#   3. Replace __PROJECT_*__ placeholders
render_template() {
    local template="$1"
    local output_file="$2"

    local content
    content=$(cat "$template")

    # Step 1: For each OTHER language, remove their entire blocks.
    local all_langs=("go" "python" "rust" "typescript")
    for lang in "${all_langs[@]}"; do
        if [[ "$lang" != "$LANG" ]]; then
            # Remove {{#lang}}...{{/lang}} blocks (including multiline)
            content=$(echo "$content" | perl -0pe "s/\{\{#$lang\}\}.*?\{\{\/$lang\}\}//gs")
        fi
    done

    # Step 2: Strip the chosen language's block markers (keep content inside).
    content=$(echo "$content" | sed "s/{{#$LANG}}//g" | sed "s/{{\/$LANG}}//g")

    # Step 3: Clean up any leftover block markers (shouldn't exist, but safety).
    content=$(echo "$content" | perl -pe 's/\{\{#\w+\}\}//g; s/\{\{\/\w+\}\}//g')

    # Step 4: Replace placeholders.
    content=$(echo "$content" | sed \
        -e "s/__PROJECT_NAME__/$NAME/g" \
        -e "s/__PROJECT_DESCRIPTION__/$DESC/g" \
        -e "s/__PROJECT_DESCRIPTION_LONG__/$DESC_LONG/g")

    # Step 5: Clean up multiple consecutive blank lines (from removed blocks).
    content=$(echo "$content" | cat -s)

    echo "$content" > "$output_file"
}

# ─── Generate ──────────────────────────────────────────────────────────────────
echo "Generating $LANG project: $NAME"
echo "  Description: $DESC"
echo "  Output:      $OUTPUT"
echo ""

# 1. Copy shared files
echo "  [1/6] Copying shared files..."
copy_tree "$SHARED_DIR" "$OUTPUT"

# 2. Copy language project files (maps directly to output root)
echo "  [2/6] Copying $LANG source files..."
PROJECT_DIR="$LANG_DIR/project"
if [[ -d "$PROJECT_DIR" ]]; then
    copy_tree "$PROJECT_DIR" "$OUTPUT"
fi

# Copy language root files (Cargo.toml, go.mod, go.sum, pyproject.toml, etc.)
for f in "$LANG_DIR"/*; do
    base=$(basename "$f")
    if [[ "$base" != "project" && "$base" != "overlays" && "$base" != "manifest.json" && "$base" != ".git" ]]; then
        cp -r "$f" "$OUTPUT/"
    fi
done

# 3. Copy overlays (Makefile, .gitignore, workflows, linter configs, etc.)
echo "  [3/6] Applying $LANG overlays..."
OVERLAY_DIR="$LANG_DIR/overlays"
if [[ -d "$OVERLAY_DIR" ]]; then
    # Copy overlay files, preserving directory structure
    rsync -a "$OVERLAY_DIR/" "$OUTPUT/"
fi

# 4. Merge .gitignore: language-specific + shared common
echo "  [4/6] Merging .gitignore..."
if [[ -f "$OUTPUT/.gitignore" ]]; then
    # Append shared common patterns
    cat "$SHARED_DIR/.gitignore.common" >> "$OUTPUT/.gitignore"
    # Deduplicate while preserving order
    awk '!seen[$0]++' "$OUTPUT/.gitignore" > "$OUTPUT/.gitignore.tmp"
    mv "$OUTPUT/.gitignore.tmp" "$OUTPUT/.gitignore"
fi

# 5. Render templates
echo "  [5/6] Rendering templates..."
for tmpl in "$TEMPLATES_DIR"/*.tmpl; do
    base=$(basename "$tmpl" .tmpl)
    render_template "$tmpl" "$OUTPUT/$base"
done

# 6. Replace placeholders in all generated files
echo "  [6/6] Replacing placeholders..."
find "$OUTPUT" -type f \
    -not -path '*/.git/*' \
    -not -path '*/node_modules/*' \
    -not -name '*.png' \
    -not -name '*.jpg' \
    -not -name '*.svg' \
    -not -name '*.ico' \
    -print0 | while IFS= read -r -d '' file; do
    # Skip binary files
    if file "$file" | grep -q "text\|empty"; then
        sed -i.bak \
            -e "s/__PROJECT_NAME__/$NAME/g" \
            -e "s/__PROJECT_DESCRIPTION__/$DESC/g" \
            -e "s/__PROJECT_DESCRIPTION_LONG__/$DESC_LONG/g" \
            "$file"
        rm -f "${file}.bak"
    fi
done

# Rename any files/dirs that contain __PROJECT_NAME__
find "$OUTPUT" -depth -name '*__PROJECT_NAME__*' | while read -r path; do
    newpath=$(echo "$path" | sed "s/__PROJECT_NAME__/$NAME/g")
    mv "$path" "$newpath"
done

echo ""
echo "  ✓ Project generated at: $OUTPUT"
echo ""
echo "Next steps:"
echo "  cd $OUTPUT"
if [[ "$LANG" == "go" ]]; then
    echo "  rm go.mod go.sum && go mod init github.com/dotbrains/$NAME && go mod tidy"
fi
echo "  make build"
echo "  make test"
