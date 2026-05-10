#!/bin/bash
# Fetch ALL remaining PISRS collections (optimized), push after each group, then power off.
# Requires GH_TOKEN env var or ~/.gh_token file.
set -e
cd /data/T.R.U.B.A.R.

TOKEN="${GH_TOKEN:-$(cat ~/.gh_token 2>/dev/null)}"
if [ -z "$TOKEN" ]; then
  echo "ERROR: set GH_TOKEN or create ~/.gh_token" >&2
  exit 1
fi

LOG=fetch_all.log

push_to_github() {
  echo "=== Pushing to GitHub $(date) ===" | tee -a "$LOG"
  git remote set-url origin "https://${TOKEN}@github.com/TomoTesten/trubar.git"
  git push origin master 2>&1 | tee -a "$LOG" || true
  git remote set-url origin https://github.com/TomoTesten/trubar.git
}

echo "=== ALL REMAINING FETCH STARTED $(date) ===" | tee -a "$LOG"

# ── Resume interrupted collection ────────────────────────────────────────────

echo "--- Neveljavni predpisi (resume ~1,956 remaining) ---" | tee -a "$LOG"
python3 fetch_pisrs.py --zbirka "Neveljavni predpisi" --workers 8 2>&1 | tee -a "$LOG"

# ── Larger regular collections ────────────────────────────────────────────────

echo "--- Neuradna prečiščena besedila lokalnih skupnosti (71k NPBs) ---" | tee -a "$LOG"
python3 fetch_pisrs.py --zbirka "Neuradna prečiščena besedila lokalnih skupnosti" --workers 8 2>&1 | tee -a "$LOG"
push_to_github

echo "--- Neveljavni akti lokalnih skupnosti (26k) ---" | tee -a "$LOG"
python3 fetch_pisrs.py --zbirka "Neveljavni akti lokalnih skupnosti" --workers 8 2>&1 | tee -a "$LOG"

echo "--- Elektronska evidenca mednarodnih aktov (5.9k) ---" | tee -a "$LOG"
python3 fetch_pisrs.py --zbirka "Elektronska evidenca mednarodnih aktov" --workers 8 2>&1 | tee -a "$LOG"

echo "--- Neuradna prečiščena besedila (70k — NPBs for state predpisi) ---" | tee -a "$LOG"
python3 fetch_pisrs.py --zbirka "Neuradna prečiščena besedila" --workers 8 2>&1 | tee -a "$LOG"

push_to_github

# ── Small extra collections ───────────────────────────────────────────────────

echo "--- Obsoletni in konzumirani predpisi (1.5k) ---" | tee -a "$LOG"
python3 fetch_pisrs.py --zbirka "Obsoletni in konzumirani predpisi" --workers 8 2>&1 | tee -a "$LOG"

echo "--- Predpisi v pripravi (1.3k) ---" | tee -a "$LOG"
python3 fetch_pisrs.py --zbirka "Predpisi v pripravi" --workers 8 2>&1 | tee -a "$LOG"

echo "--- Akti lokalnih skupnosti v pripravi (2.1k) ---" | tee -a "$LOG"
python3 fetch_pisrs.py --zbirka "Akti lokalnih skupnosti v pripravi" --workers 8 2>&1 | tee -a "$LOG"

echo "--- Postopki proti RS (769) ---" | tee -a "$LOG"
python3 fetch_pisrs.py --zbirka "Postopki proti RS" --workers 8 2>&1 | tee -a "$LOG"

echo "--- Predhodna vprašanja (43) ---" | tee -a "$LOG"
python3 fetch_pisrs.py --zbirka "Predhodna vprašanja" --workers 8 2>&1 | tee -a "$LOG"

push_to_github

# ── Court decisions → Hugging Face (not git) ─────────────────────────────────

HF_TOKEN="${HF_TOKEN:-$(cat ~/.hf_token 2>/dev/null)}"
if [ -z "$HF_TOKEN" ]; then
  echo "WARNING: no HF_TOKEN — court decisions will be cached locally only (--dry-run)" | tee -a "$LOG"
  HF_FLAG="--dry-run"
else
  HF_FLAG=""
fi

echo "--- Court decisions + Constitutional Court → HF dataset ---" | tee -a "$LOG"
python3 fetch_court_hf.py --hf-repo TomoTesten/trubar-sodna-praksa --workers 12 $HF_FLAG 2>&1 | tee -a "$LOG"

echo "=== ALL PISRS+COURT DONE $(date) ===" | tee -a "$LOG"

# ── DZ open data (all mandates) — commit to git ───────────────────────────────

echo "--- DZ open data (VPP, PZ, GDZ, SDT/SDZ — all mandates) ---" | tee -a "$LOG"
python3 fetch_dz_opendata.py --skip-ul --workers 6 2>&1 | tee -a "$LOG"

echo "--- Committing dz/ files ---" | tee -a "$LOG"
git add dz/ 2>&1 | tee -a "$LOG"
git commit -m "Add DZ open data (parliamentary questions, bill proposals, voting records)" 2>&1 | tee -a "$LOG" || true
push_to_github

echo "=== ALL DONE $(date) ===" | tee -a "$LOG"
