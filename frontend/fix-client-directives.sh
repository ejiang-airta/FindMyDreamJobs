#!/bin/bash

# ✅ Script: fix-client-directives.sh
# 📍 Purpose: Automatically add 'use client' directive to .tsx files using client-only features

echo "🔍 Scanning for .tsx files that use React client-only features but lack 'use client'..."

# Step 1: Find matching files
FILES=$(grep -El 'use(State|Effect|Ref|Context)|localStorage|window|document' src/**/*.* \
  | xargs grep -L "'use client'")

if [ -z "$FILES" ]; then
  echo "✅ All files are already correctly using 'use client'."
  exit 0
fi

echo "⚠️ The following files are missing 'use client':"
echo "$FILES"
echo

read -p "Do you want to add 'use client' to these files? (y/n): " confirm
if [[ "$confirm" != "y" ]]; then
  echo "❌ Aborted. No changes were made."
  exit 1
fi

echo "✏️ Adding 'use client' to selected files..."

# Step 2: Update each file safely
for file in $FILES; do
  tmp_file=$(mktemp)
  inserted=0
  while IFS= read -r line; do
    if [[ $inserted -eq 0 && ! "$line" =~ ^[[:space:]]*// ]]; then
      echo "'use client'" > "$tmp_file"
      echo "$line" >> "$tmp_file"
      inserted=1
    else
      echo "$line" >> "$tmp_file"
    fi
  done < "$file"
  mv "$tmp_file" "$file"
  echo "✅ Updated: $file"
done

echo "🎉 All matching files are now updated!"