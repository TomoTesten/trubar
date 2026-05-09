#!/bin/bash
# Fetch all remaining PISRS collections and push to GitHub.
# Requires GH_TOKEN env var or ~/.gh_token file with a public_repo PAT.
set -e
cd /data/T.R.U.B.A.R.

TOKEN="${GH_TOKEN:-$(cat ~/.gh_token 2>/dev/null)}"
if [ -z "$TOKEN" ]; then
  echo "ERROR: set GH_TOKEN or create ~/.gh_token" >&2
  exit 1
fi

LOG=fetch_pisrs.log
echo "=== PISRS FETCH STARTED $(date) ===" | tee -a "$LOG"

python3 fetch_pisrs.py --zbirka "Veljavni akti lokalnih skupnosti" --delay 0.3 2>&1 | tee -a "$LOG"
python3 fetch_pisrs.py --zbirka "Drugi splošni in posamični akti"   --delay 0.3 2>&1 | tee -a "$LOG"
python3 fetch_pisrs.py --zbirka "Splošni akti za izvrševanje javnih pooblastil" --delay 0.3 2>&1 | tee -a "$LOG"

echo "=== FETCH DONE $(date), pushing ===" | tee -a "$LOG"

git remote set-url origin "https://${TOKEN}@github.com/TomoTesten/trubar.git"
git push origin master 2>&1 | tee -a "$LOG"
git remote set-url origin https://github.com/TomoTesten/trubar.git

echo "=== ALL DONE $(date) ===" | tee -a "$LOG"
