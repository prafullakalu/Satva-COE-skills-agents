#!/usr/bin/env sh
# Installs the Satva skills (and optionally agents) into Claude Code (macOS, Linux, Git Bash, WSL).
# Skills live nested by department in this repo (skills/<dept>/<group>/<skill>); Claude Code needs them flat,
# so each skill folder is copied to <target>/<skill-name>.
#   ./install.sh                         all skills        -> ~/.claude/skills   (every project)
#   ./install.sh --dept accounting,seo   only those departments (accounting marketing seo satva general)
#   ./install.sh --only xero-bank-reconciliation,satva-doc
#   ./install.sh --agents                also agents       -> ~/.claude/agents   (honours --dept)
#   ./install.sh --project               into ./.claude/skills (and ./.claude/agents) for this project only
#   ./install.sh --target /some/folder   skills there; agents go to its sibling "agents" folder
#   ./install.sh --list                  show what is available, install nothing
# Re-running upgrades in place. Files removed from a newer version are NOT deleted from an old install.
set -eu
here=$(cd "$(dirname "$0")" && pwd)
target="$HOME/.claude/skills"; atarget=""; only=""; dept=""; agents=0; list=0
while [ $# -gt 0 ]; do
  case "$1" in
    --project) target="$(pwd)/.claude/skills" ;;
    --target)  shift; target="$1" ;;
    --only)    shift; only=",$1," ;;
    --dept)    shift; dept=",$1," ;;
    --agents)  agents=1 ;;
    --list)    list=1 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac; shift
done
[ -n "$atarget" ] || atarget="$(dirname "$target")/agents"
want() { # $1 = department, $2 = name
  [ -z "$dept" ] || case "$dept" in *",$1,"*) ;; *) return 1 ;; esac
  [ -z "$only" ] || case "$only" in *",$2,"*) ;; *) return 1 ;; esac
}
[ "$list" = 1 ] || mkdir -p "$target"
find "$here/skills" -name SKILL.md | sort | while read -r f; do
  d=$(dirname "$f"); name=$(basename "$d"); rel=${d#"$here"/skills/}; dd=${rel%%/*}
  want "$dd" "$name" || continue
  if [ "$list" = 1 ]; then printf '%-11s %-42s %s\n' "$dd" "$name" "skills/$rel"; continue; fi
  mkdir -p "$target/$name"
  cp -R "$d/." "$target/$name/"          # contents, never the folder itself
  echo "installed  $name  ->  $target/$name"
done
if [ "$agents" = 1 ] && [ -d "$here/agents" ]; then
  for f in "$here"/agents/*/*.md; do
    [ -f "$f" ] || continue
    [ "$(basename "$f")" = "README.md" ] && continue
    dd=$(basename "$(dirname "$f")"); name=$(basename "$f" .md)
    want "$dd" "$name" || continue
    if [ "$list" = 1 ]; then printf '%-11s %-42s %s\n' "$dd" "$name" "agent"; continue; fi
    mkdir -p "$atarget"; cp "$f" "$atarget/"; echo "installed  agent $name  ->  $atarget"
  done
fi
[ "$list" = 1 ] || { echo; echo "Done. Restart Claude Code (or start a new session) so it picks them up."; }
