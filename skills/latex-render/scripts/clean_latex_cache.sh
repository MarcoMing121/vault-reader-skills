#!/bin/bash

# LaTeX Cache Cleanup Script
# Cleans up cached LaTeX rendered images older than specified hours
#
# Usage: clean_latex_cache.sh <hours>
# Example: clean_latex_cache.sh 24  (removes files older than 24 hours)

CACHE_DIR="/root/.openclaw/shared/latex-cache"
HOURS=${1:-24}

# Create directories if they don't exist
mkdir -p "$CACHE_DIR"

# Check if cache directory exists
if [ ! -d "$CACHE_DIR" ]; then
    echo "Error: Cache directory does not exist: $CACHE_DIR"
    exit 1
fi

# Count files before cleanup
TOTAL_BEFORE=$(find "$CACHE_DIR" -type f | wc -l)

# Find and delete files older than specified hours
DELETED=$(find "$CACHE_DIR" -type f -mtime +$((HOURS / 24)) -print 2>/dev/null | wc -l)

# Actually delete the files
find "$CACHE_DIR" -type f -mtime +$((HOURS / 24)) -delete 2>/dev/null

# Count files after cleanup
TOTAL_AFTER=$(find "$CACHE_DIR" -type f | wc -l)

echo "Latex cache cleanup completed:"
echo "  Files deleted: $DELETED"
echo "  Remaining files: $TOTAL_AFTER"
echo "  Threshold: $HOURS hours"

exit 0
