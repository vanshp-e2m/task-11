#!/usr/bin/env bash
# Usage: tools/snapshot.sh <label>   → backups/NN-<label>.sql (numbered, never overwrites)
set -e
cd "$(dirname "$0")/.."
mkdir -p backups
label="${1:?usage: tools/snapshot.sh <label>}"
n=$(printf '%02d' "$(ls backups/*.sql 2>/dev/null | wc -l)")
out="backups/${n}-${label}.sql"
tools/wp.sh db export "$out" >/dev/null
echo "snapshot: $out ($(du -h "$out" | cut -f1))"
