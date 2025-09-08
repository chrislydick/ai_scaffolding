#!/usr/bin/env bash
set -euo pipefail
ALLOWLIST_REGEX='(\.png|\.jpg|\.jpeg|\.gif|\.ico|\.pdf|\.svg|\.woff2?)$'
BAD=0
while read -r f; do
  [[ $f =~ $ALLOWLIST_REGEX ]] && continue
  if file "$f" | grep -qiE 'executable|ELF|PE32|COFF|Mach-O|archive'; then
    echo "ERROR: binary/executable detected: $f"
    BAD=1
  fi
  if xxd -p "$f" | grep -qiE '([0-9a-f]{2}){64,}'; then
    STRS=$(strings "$f" | wc -l || true)
    if [[ "$STRS" -lt 2 ]]; then
      echo "ERROR: likely encoded/binary content: $f"
      BAD=1
    fi
  fi
done < <(git ls-files)
exit $BAD

