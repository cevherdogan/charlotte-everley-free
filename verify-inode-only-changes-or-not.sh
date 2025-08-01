git diff --name-only --cached --diff-filter=M | while read file; do
  git diff --cached "$file" >/dev/null || echo "Changed: $file"
done


