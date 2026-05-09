#!/bin/bash
# Run the podzakonski fetch and push results to GitHub when done.
# Requires GH_TOKEN env var or ~/.gh_token file with a public_repo PAT.
# Logs to /data/T.R.U.B.A.R./fetch_podzakonski.log
set -e
cd /data/T.R.U.B.A.R.

TOKEN="${GH_TOKEN:-$(cat ~/.gh_token 2>/dev/null)}"
if [ -z "$TOKEN" ]; then
  echo "ERROR: set GH_TOKEN or create ~/.gh_token" >&2
  exit 1
fi

echo "=== STARTED $(date) ===" | tee -a fetch_podzakonski.log

python3 fetch_podzakonski.py --delay 0.4 2>&1 | tee -a fetch_podzakonski.log

echo "=== FETCH DONE $(date), pushing to GitHub ===" | tee -a fetch_podzakonski.log

git remote set-url origin "https://${TOKEN}@github.com/TomoTesten/trubar.git"
git push origin master 2>&1 | tee -a fetch_podzakonski.log
git remote set-url origin https://github.com/TomoTesten/trubar.git

echo "=== ALL DONE $(date) ===" | tee -a fetch_podzakonski.log
