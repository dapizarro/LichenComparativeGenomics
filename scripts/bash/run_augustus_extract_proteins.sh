#!/usr/bin/env bash
set -euo pipefail
GENOME="$1"
SAMPLE="$2"
GFF="$3"
PROT="$4"
SPECIES="$5"
mkdir -p "$(dirname "$GFF")" "$(dirname "$PROT")"
augustus --species="$SPECIES" --gff3=on "$GENOME" > "$GFF"
# Minimal protein extraction from AUGUSTUS comments
awk '/^# protein sequence =/ {flag=1; seq=$0; gsub(/^# protein sequence = \[/,"",seq); gsub(/\]/,"",seq); print ">" ++i; print seq; next} flag && /^#/ {seq=$0; gsub(/^# /,"",seq); gsub(/\]/,"",seq); print seq; if ($0 ~ /\]/) flag=0}' "$GFF" > "$PROT" || true
