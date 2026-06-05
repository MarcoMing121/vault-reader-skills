#!/bin/bash
# Clean old LaTeX cache images
# Usage: ./clean_latex_cache.sh [max_age_hours]

# Read cache path from config
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/../../_shared/user-config.json"

if [ -f "$CONFIG_FILE" ]; then
    CACHE_DIR=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('LATEX_CACHE_PATH', '/root/.openclaw/shared/latex-cache'))")
else
    CACHE_DIR="/root/.openclaw/shared/latex-cache"
fi

MAX_AGE_HOURS=${1:-24}  # Default: 24 hours

if [ ! -d "$CACHE_DIR" ]; then
    echo "Cache directory does not exist: $CACHE_DIR"
    exit 0
fi

# Find and delete files older than MAX_AGE_HOURS
echo "Cleaning latex-cache (files older than $MAX_AGE_HOURS hours)..."

DELETED_COUNT=$(find "$CACHE_DIR" -name "*.png" -mmin +$((MAX_AGE_HOURS * 60)) -delete -print | wc -l)

echo "Deleted $DELETED_COUNT files"

# Show remaining files
REMAINING=$(find "$CACHE_DIR" -name "*.png" | wc -l)
echo "Remaining: $REMAINING files in cache"

# Show disk usage
du -sh "$CACHE_DIR" 2>/dev/null || echo "Cache empty or not accessible"
