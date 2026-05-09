#!/bin/bash
# Requires GH_TOKEN env var or ~/.gh_token file with a public_repo PAT.
set -e
cd /data/T.R.U.B.A.R.

TOKEN="${GH_TOKEN:-$(cat ~/.gh_token 2>/dev/null)}"
if [ -z "$TOKEN" ]; then
  echo "ERROR: set GH_TOKEN or create ~/.gh_token" >&2
  exit 1
fi

echo "=== NPB FETCH STARTED $(date) ===" | tee -a fetch_npb.log

python3 fetch_npb.py --delay 0.3 2>&1 | tee -a fetch_npb.log

echo "=== NPB FETCH DONE $(date), pushing ===" | tee -a fetch_npb.log

git remote set-url origin "https://${TOKEN}@github.com/TomoTesten/trubar.git"
git push origin master 2>&1 | tee -a fetch_npb.log
git remote set-url origin https://github.com/TomoTesten/trubar.git

echo "=== ALL DONE $(date) ===" | tee -a fetch_npb.log
