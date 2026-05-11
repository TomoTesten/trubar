# T.R.U.B.A.R. Overnight Handoff

## What is running right now

**PID 148716** — `python3 fetch_court_hf.py --hf-repo TomoTesten/trubar-sodna-praksa --workers 12`
- Uploading ~254k court decisions to Hugging Face as Parquet shards
- Already uploading shard 0002 for "Sodna praksa Višjega delovnega in socialnega sodišča"
- Progress is saved in `.progress_court_hf_*.txt` files — restarts automatically from where it left off
- ETA: ~15–18 hours total
- Log: `fetch_all.log` (tail it to check progress)

## What needs to happen overnight

1. **Monitor HF upload** — check every ~30 min that PID 148716 is still alive
   - If dead: `cd /data/T.R.U.B.A.R. && nohup python3 fetch_court_hf.py --hf-repo TomoTesten/trubar-sodna-praksa --workers 12 >> fetch_all.log 2>&1 &`
   - It resumes automatically from progress files

2. **GitHub Pages** — needs to be enabled manually by the user (can't do via API with current token):
   - github.com/TomoTesten/trubar → Settings → Pages → Source: master branch, /docs folder

3. **GitHub Actions workflow** — needs a token with `workflow` scope to push:
   - File is at: `/data/T.R.U.B.A.R./.github/workflows/build-site.yml`
   - Once user upgrades token, run: `cd /data/T.R.U.B.A.R. && git add .github/ && git commit -m "Add GitHub Actions auto-rebuild workflow" && git push origin master`

4. **Git gc** — pack loose objects to shrink repo size:
   - `cd /data/T.R.U.B.A.R. && git gc --aggressive --prune=now`
   - Safe to run anytime, takes ~5–10 min

5. **After HF upload completes** — do a final GitHub push:
   - `cd /data/T.R.U.B.A.R. && git add . && git status` (check nothing sensitive)
   - Then push with token

## Current state of the data

- **GitHub** (`TomoTesten/trubar`): all laws pushed ✅
  - 43,774 static site pages in `docs/`
  - DZ parliamentary data in `dz/`
  - All legislation in `si/`
- **Hugging Face** (`TomoTesten/trubar-sodna-praksa`): uploading now 🔄
- **Search index** (Pagefind): NOT YET built — will build via GitHub Actions once workflow is pushed

## How to check HF upload progress

```bash
tail -20 /data/T.R.U.B.A.R./fetch_all.log
ps aux | grep fetch_court | grep -v grep
```

## Token locations

- GitHub: `~/.gh_token`
- Hugging Face: `~/.hf_token`

## Repo location

`/data/T.R.U.B.A.R.`
