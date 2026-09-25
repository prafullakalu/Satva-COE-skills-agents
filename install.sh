#!/usr/bin/env sh
# Installs the Satva skills into Claude Code (macOS, Linux, Git Bash, WSL).
#   ./install.sh                       all skills -> ~/.claude/skills   (every project)
#   ./install.sh --project             all skills -> ./.claude/skills   (this project only)
#   ./install.sh --only satva-guide-gif,satva-doc
#   ./install.sh --target /some/folder
# Re-running upgrades in place. Files removed from a newer version are NOT deleted from an old install.
set -eu
here=$(cd "$(dirname "$0")" && pwd)
target="$HOME/.claude/skills"; only=""
while [ $# -gt 0 ]; do
  case "$1" in
    --project) target="$(pwd)/.claude/skills" ;;
    --target)  shift; target="$1" ;;
    --only)    shift; only=",$1," ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac; shift
done
mkdir -p "$target"
for d in "$here"/skills/*/; do
  name=$(basename "$d")
  [ -n "$only" ] && case "$only" in *",$name,"*) ;; *) continue ;; esac
  mkdir -p "$target/$name"
  cp -R "$d." "$target/$name/"          # contents, never the folder itself
  echo "installed  $name  ->  $target/$name"
done
echo; echo "Done. Restart Claude Code (or start a new session) so it picks the skills up."
