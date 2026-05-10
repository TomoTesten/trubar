#!/bin/bash
# Fetch ALL remaining PISRS collections, push after each one, then power off.
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

# ── Fast collections first ────────────────────────────────────────────────────

echo "--- Neuradna prečiščena besedila lokalnih skupnosti (71k NPBs) ---" | tee -a "$LOG"
python3 fetch_pisrs.py --zbirka "Neuradna prečiščena besedila lokalnih skupnosti" --delay 0.2 2>&1 | tee -a "$LOG"
push_to_github

echo "--- Neveljavni predpisi (16k) ---" | tee -a "$LOG"
python3 fetch_pisrs.py --zbirka "Neveljavni predpisi" --delay 0.2 2>&1 | tee -a "$LOG"

echo "--- Neveljavni akti lokalnih skupnosti (26k) ---" | tee -a "$LOG"
python3 fetch_pisrs.py --zbirka "Neveljavni akti lokalnih skupnosti" --delay 0.2 2>&1 | tee -a "$LOG"

echo "--- Elektronska evidenca mednarodnih aktov (5.9k) ---" | tee -a "$LOG"
python3 fetch_pisrs.py --zbirka "Elektronska evidenca mednarodnih aktov" --delay 0.2 2>&1 | tee -a "$LOG"

echo "--- Neuradna prečiščena besedila (70k — NPBs for state predpisi) ---" | tee -a "$LOG"
python3 fetch_pisrs.py --zbirka "Neuradna prečiščena besedila" --delay 0.2 2>&1 | tee -a "$LOG"

push_to_github

# ── Court decisions (slow — sodnapraksa.si fetch per item) ────────────────────

echo "--- Sodna praksa Vrhovnega sodišča (66k) ---" | tee -a "$LOG"
python3 fetch_pisrs.py --zbirka "Sodna praksa Vrhovnega sodišča" --delay 0.0 2>&1 | tee -a "$LOG"
push_to_github

echo "--- Sodna praksa Upravnega sodišča (35k) ---" | tee -a "$LOG"
python3 fetch_pisrs.py --zbirka "Sodna praksa Upravnega sodišča" --delay 0.0 2>&1 | tee -a "$LOG"
push_to_github

echo "--- Sodna praksa Višjega delovnega in socialnega sodišča (26k) ---" | tee -a "$LOG"
python3 fetch_pisrs.py --zbirka "Sodna praksa Višjega delovnega in socialnega sodišča" --delay 0.0 2>&1 | tee -a "$LOG"
push_to_github

echo "--- Sodna praksa višjih sodišč (101k) ---" | tee -a "$LOG"
python3 fetch_pisrs.py --zbirka "Sodna praksa višjih sodišč" --delay 0.0 2>&1 | tee -a "$LOG"
push_to_github

echo "=== ALL DONE $(date) ===" | tee -a "$LOG"

# ── Power off ─────────────────────────────────────────────────────────────────
echo "Powering off..." | tee -a "$LOG"
sudo systemctl poweroff
