#!/usr/bin/env bash
set -euo pipefail

[[ $# -eq 2 ]] || { echo "usage: $0 <language> <destination>" >&2; exit 2; }

repo=$(cd "$(dirname "$0")/.." && pwd)
git -C "$repo" cat-file -e "HEAD:template/$1" 2>/dev/null \
    || { echo "error: no template for '$1'" >&2; exit 1; }

if [[ -e $2 ]]; then
    echo "error: $2 already exists" >&2
    exit 1
fi

mkdir -p "$2"
git -C "$repo" archive "HEAD:template/$1" | tar -x -C "$2"
echo "copied template/$1 to $2"
