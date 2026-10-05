#!/bin/bash
# Run all SPARQL templates for Kuwait (Q817) with rate limiting >=12s
OUT="D:/claude-workspace/apec-osint-tool/output/kw/2026-10-03/raw"
QDIR="D:/claude-workspace/apec-osint-tool/output/kw/2026-10-03/queries"
UA="APEC-OSINT-Research/1.0 (contact: research@example.org)"
mkdir -p "$OUT"

run_q() {
  local name="$1"
  local file="$2"
  echo "=== $name start $(date +%T) ==="
  curl --proxy "http://127.0.0.1:7890" -s -L --max-time 120 \
    -H "User-Agent: $UA" \
    -H "Accept: application/sparql-results+json" \
    --data-urlencode "query@${file}" \
    "https://query.wikidata.org/sparql" \
    -o "${OUT}/${name}.json"
  local size=$(stat -c%s "${OUT}/${name}.json" 2>/dev/null || echo 0)
  echo "=== $name done size=${size} $(date +%T) ==="
  sleep 13
}

run_q "H_state_powers"  "$QDIR/H_state_powers.rq"
run_q "A_general"       "$QDIR/A_general.rq"
run_q "B_corp"          "$QDIR/B_corp.rq"
run_q "C_acad"          "$QDIR/C_acad.rq"
run_q "D_party"         "$QDIR/D_party.rq"
run_q "E_media"         "$QDIR/E_media.rq"
run_q "F_fin"           "$QDIR/F_fin.rq"
echo "ALL DONE"
