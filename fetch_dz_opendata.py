#!/usr/bin/env python3
"""
T.R.U.B.A.R. — Državni zbor open data fetcher

Downloads and converts all DZ open data XML files (all mandates) into Markdown:
  VPP{n}.XML  — parliamentary questions (mandates 2-10, ~28k total)
  PZ{n}.XML   — bill proposals (mandates 2-10)
  GDZ{n}.XML  — National Assembly voting records (mandates 3-10)
  GDT{n}.XML  — Working body voting records (mandates 8-10)
  SDT{n}.XML  — Working body session index (mandates 2-10)
  SDZ{n}.XML  — National Assembly session index (mandates 2-10)

Files go into dz/ directory. NO git commits — batch-commit separately.

Usage:
  python fetch_dz_opendata.py [--skip-ul] [--workers 6] [--only VPP,PZ]
"""

import xml.etree.ElementTree as ET
import json, re, os, time, argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import threading

import requests

import sys
sys.path.insert(0, str(Path(__file__).parent))
from fetch import REPO_DIR, fetch_ul_html, html_to_markdown

DZ_BASE  = "https://fotogalerija.dz-rs.si/datoteke/opendata"
OUT_DIR  = REPO_DIR / "dz"
HEADERS  = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0"}

# All available mandate files (discovered by probing)
DZ_MANDATES = {
    "VPP": list(range(2, 11)),   # VPP2..VPP10 (VPP.XML = mandat 10)
    "PZ":  list(range(2, 11)),
    "GDZ": list(range(3, 11)),
    "GDT": list(range(8, 11)),
    "SDT": list(range(2, 11)),
    "SDZ": list(range(2, 11)),
}

_SAFE_RE   = re.compile(r"[^a-zA-Z0-9_-]")
_prog_lock = threading.Lock()


def safe(s):
    return _SAFE_RE.sub("_", s or "")


def esc(s):
    return (s or "").replace('"', '\\"')


def xml_url(prefix, mandat):
    # mandat 10 = current = no number suffix (VPP.XML), others = VPP2.XML etc.
    suffix = "" if mandat == 10 else str(mandat)
    return f"{DZ_BASE}/{prefix}{suffix}.XML"


# ── XML download ──────────────────────────────────────────────────────────────

def download_xml(prefix, mandat):
    suffix = "" if mandat == 10 else str(mandat)
    cache  = REPO_DIR / f".dz_{prefix}{suffix}.xml"
    url    = xml_url(prefix, mandat)
    if cache.exists():
        return ET.parse(str(cache)).getroot()
    print(f"  Downloading {prefix}{suffix}.XML ...")
    r = requests.get(url, headers=HEADERS, timeout=120)
    r.raise_for_status()
    cache.write_bytes(r.content)
    print(f"  {prefix}{suffix}.XML: {len(r.content)//1024} KB")
    return ET.fromstring(r.content)


# ── Progress ──────────────────────────────────────────────────────────────────

def progress_file(name):
    return REPO_DIR / f".progress_dz_{name}.txt"


def load_progress(name):
    pf = progress_file(name)
    return set(pf.read_text().splitlines()) if pf.exists() else set()


def save_progress(name, item_id):
    with _prog_lock:
        with open(progress_file(name), "a") as f:
            f.write(item_id + "\n")


# ── VPP — Parliamentary questions ─────────────────────────────────────────────

def process_vpp(done, dry_run):
    out = OUT_DIR / "vprasanja"
    out.mkdir(parents=True, exist_ok=True)
    ok = skip = 0

    for mandat in DZ_MANDATES["VPP"]:
        try:
            root = download_xml("VPP", mandat)
        except Exception as e:
            print(f"  VPP mandat {mandat}: skip ({e})")
            continue

        items = root.findall("VPRASANJE")
        print(f"  VPP mandat {mandat}: {len(items)} questions")

        for item in items:
            k      = item.find("KARTICA_VPRASANJA")
            unid   = (k.findtext("UNID") or "").strip().split("|")[-1].strip()
            naslov = k.findtext("KARTICA_NASLOV") or ""
            datum  = k.findtext("KARTICA_DATUM") or ""
            vrsta  = k.findtext("KARTICA_VRSTA") or ""
            vlaga  = k.findtext("KARTICA_VLAGATELJ") or ""
            pskg   = k.findtext("KARTICA_POSLANSKA_SKUPINA") or ""
            naslov_enc = k.findtext("KARTICA_NASLOVLJENEC") or ""
            status = k.findtext("KARTICA_STATUS") or ""

            item_id = unid or f"vpp_{mandat}_{ok+skip}"
            if item_id in done:
                skip += 1
                continue

            slug = f"vpp-{safe(item_id)}"
            fm = (
                "---\n"
                f'unid: "{esc(item_id)}"\n'
                f'vrsta: "{esc(vrsta)}"\n'
                f'naslov: "{esc(naslov)}"\n'
                f'datum: "{esc(datum)}"\n'
                f'vlagatelj: "{esc(vlaga)}"\n'
                f'poslanska_skupina: "{esc(pskg)}"\n'
                f'naslovljenec: "{esc(naslov_enc)}"\n'
                f'status: "{esc(status)}"\n'
                f'mandat: {mandat}\n'
                'zbirka: "Parlamentarna vprašanja DZ"\n'
                f'vir: "https://www.dz-rs.si/wps/portal/Home/deloDZ/vprasanjaposlancev/vprasanje?unid={esc(item_id)}"\n'
                "---\n"
            )
            body = f"# {naslov}\n\n"
            body += f"**Vlagatelj:** {vlaga}  \n"
            body += f"**Poslanska skupina:** {pskg}  \n"
            body += f"**Naslovljenec:** {naslov_enc}  \n"
            body += f"**Datum:** {datum}  \n"
            body += f"**Status:** {status}  \n"
            body += f"**Vrsta:** {vrsta}  \n\n"

            pod = item.find("PODDOKUMENTI")
            if pod is not None:
                pod_ids = [u.text.strip().split("|")[-1].strip()
                           for u in pod.findall("UNID") if u.text]
                if pod_ids:
                    body += "## Poddokumenti\n\n"
                    for pid in pod_ids:
                        body += f"- {pid}\n"
                    body += "\n"

            if not dry_run:
                (out / f"{slug}.md").write_text(fm + body, encoding="utf-8")
                save_progress("VPP", item_id)
            ok += 1

    print(f"VPP total: {ok} written, {skip} skipped")


# ── PZ — Bill proposals ───────────────────────────────────────────────────────

def _pz_write(item, mandat, out, dry_run, fetch_ul_text):
    k      = item.find("KARTICA_PREDPISA")
    unid   = (k.findtext("UNID") or "").strip().split("|")[-1].strip()
    epa    = k.findtext("KARTICA_EPA") or ""
    kratica = k.findtext("KARTICA_KRATICA") or ""
    naziv  = k.findtext("KARTICA_NAZIV") or ""
    datum  = k.findtext("KARTICA_DATUM") or ""
    predl  = k.findtext("KARTICA_PREDLAGATELJ") or ""
    postop = k.findtext("KARTICA_POSTOPEK") or ""
    faza   = k.findtext("KARTICA_FAZA_POSTOPKA") or ""
    sop    = k.findtext("KARTICA_SOP") or ""
    kljucne = k.findtext("KARTICA_KLJUCNE_BESEDE") or ""

    item_id = epa or unid
    slug    = f"pz-{safe(item_id)}"
    fm = (
        "---\n"
        f'unid: "{esc(unid)}"\n'
        f'epa: "{esc(epa)}"\n'
        f'kratica: "{esc(kratica)}"\n'
        f'naziv: "{esc(naziv)}"\n'
        f'datum: "{esc(datum)}"\n'
        f'predlagatelj: "{esc(predl)}"\n'
        f'postopek: "{esc(postop)}"\n'
        f'faza: "{esc(faza)}"\n'
        f'sop: "{esc(sop)}"\n'
        f'mandat: {mandat}\n'
        'zbirka: "Predlogi zakonov DZ"\n'
        "---\n"
    )
    body = f"# {naziv}\n\n"
    body += f"**EPA:** {epa}  \n**Predlagatelj:** {predl}  \n"
    body += f"**Postopek:** {postop}  \n**Faza:** {faza}  \n**Datum:** {datum}  \n\n"
    if kljucne:
        body += f"**Ključne besede:** {kljucne}  \n\n"

    if sop and fetch_ul_text:
        try:
            html = fetch_ul_html(sop)
            if html:
                md = html_to_markdown(html)
                if md:
                    body += "## Besedilo\n\n" + md + "\n"
        except Exception:
            pass

    if not dry_run:
        (out / f"{slug}.md").write_text(fm + body, encoding="utf-8")
        save_progress("PZ", item_id)
    return item_id


def process_pz(done, dry_run, fetch_ul_text, workers):
    out = OUT_DIR / "predlogi_zakonov"
    out.mkdir(parents=True, exist_ok=True)
    ok = skip = fail = 0

    all_pending = []
    for mandat in DZ_MANDATES["PZ"]:
        try:
            root = download_xml("PZ", mandat)
        except Exception as e:
            print(f"  PZ mandat {mandat}: skip ({e})")
            continue
        items = root.findall("PREDPIS")
        print(f"  PZ mandat {mandat}: {len(items)} proposals")
        for item in items:
            k = item.find("KARTICA_PREDPISA")
            unid = (k.findtext("UNID") or "").strip().split("|")[-1].strip()
            epa  = k.findtext("KARTICA_EPA") or ""
            item_id = epa or unid
            if item_id in done:
                skip += 1
            else:
                all_pending.append((item, mandat, item_id))

    print(f"PZ pending: {len(all_pending)}, skipped: {skip}")

    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(_pz_write, item, mandat, out, dry_run, fetch_ul_text): iid
                   for item, mandat, iid in all_pending}
        n = 0
        for future in as_completed(futures):
            n += 1
            try:
                future.result()
                ok += 1
            except Exception as e:
                fail += 1
            if n % 1000 == 0:
                print(f"  PZ: {n}/{len(all_pending)}")

    print(f"PZ total: {ok} written, {skip} skipped, {fail} failed")


# ── GDZ / GDT — Voting records ────────────────────────────────────────────────

def _parse_votes(seznam_text):
    votes = []
    for v in (seznam_text or "").split("<VALUE>"):
        v = v.replace("</VALUE>", "").strip()
        if v:
            parts = v.split("|")
            if len(parts) == 3:
                votes.append(f"| {parts[0]} | {parts[1]} | {parts[2]} |")
    return votes


def process_voting(prefix, done, dry_run):
    out = OUT_DIR / "glasovanja"
    out.mkdir(parents=True, exist_ok=True)
    ok = skip = 0

    for mandat in DZ_MANDATES[prefix]:
        try:
            root = download_xml(prefix, mandat)
        except Exception as e:
            print(f"  {prefix} mandat {mandat}: skip ({e})")
            continue
        items = root.findall("GLASOVANJE")
        print(f"  {prefix} mandat {mandat}: {len(items)} votes")

        for item in items:
            unid   = (item.findtext("UNID") or "").strip()
            datum  = item.findtext("GLASOVANJE_DATUM_CAS") or ""
            za     = item.findtext("GLASOVANJE_ZA") or "0"
            proti  = item.findtext("GLASOVANJE_PROTI") or "0"
            kvorum = item.findtext("GLASOVANJE_KVORUM") or "0"
            naslov = item.findtext("NASLOV_AKTA") or ""
            vrsta  = item.findtext("VRSTA") or ""
            epa    = item.findtext("EPA") or ""
            seja_el = item.find("SEJA")
            seja_id = seja_el.findtext("ID") or "" if seja_el is not None else ""
            tocka_el = item.find("TOCKA")
            tocka   = tocka_el.findtext("IME") or "" if tocka_el is not None else ""
            seznam  = item.findtext("SEZNAM") or ""

            item_id = f"{prefix}_{safe(unid)}"
            if item_id in done:
                skip += 1
                continue

            votes = _parse_votes(seznam)
            fm = (
                "---\n"
                f'unid: "{esc(unid)}"\n'
                f'datum: "{esc(datum[:10] if datum else "")}"\n'
                f'naslov: "{esc(naslov)}"\n'
                f'vrsta: "{esc(vrsta)}"\n'
                f'epa: "{esc(epa)}"\n'
                f'seja: "{esc(seja_id)}"\n'
                f'za: {za}\n'
                f'proti: {proti}\n'
                f'kvorum: {kvorum}\n'
                f'mandat: {mandat}\n'
                f'zbirka: "Glasovanja {prefix}"\n'
                "---\n"
            )
            body = f"# Glasovanje: {naslov or tocka or vrsta}\n\n"
            body += f"**Datum:** {datum}  \n**Seja:** {seja_id}  \n**Točka:** {tocka}  \n\n"
            body += f"| Za | Proti | Kvorum |\n|---|---|---|\n| {za} | {proti} | {kvorum} |\n\n"
            if votes:
                body += "## Glasovi poslancev\n\n"
                body += "| Poslanec | Skupina | Glas |\n|---|---|---|\n"
                body += "\n".join(votes) + "\n"

            if not dry_run:
                (out / f"{item_id}.md").write_text(fm + body, encoding="utf-8")
                save_progress(prefix, item_id)
            ok += 1

    print(f"{prefix} total: {ok} written, {skip} skipped")


# ── SDT / SDZ — Session index ─────────────────────────────────────────────────

def process_sessions(prefix, done, dry_run):
    out = OUT_DIR / "seje"
    out.mkdir(parents=True, exist_ok=True)
    ok = skip = 0

    for mandat in DZ_MANDATES[prefix]:
        try:
            root = download_xml(prefix, mandat)
        except Exception as e:
            print(f"  {prefix} mandat {mandat}: skip ({e})")
            continue
        items = root.findall("SEJA")
        print(f"  {prefix} mandat {mandat}: {len(items)} sessions")

        for item in items:
            k      = item.find("KARTICA_SEJE")
            unid   = (k.findtext("UNID") or "").strip().split("|")[-1].strip()
            oznaka = k.findtext("KARTICA_OZNAKA") or ""
            vrsta  = k.findtext("KARTICA_VRSTA") or ""
            status = k.findtext("KARTICA_STATUS") or ""

            item_id = f"{prefix}_{safe(unid)}"
            if item_id in done:
                skip += 1
                continue

            fm = (
                "---\n"
                f'unid: "{esc(unid)}"\n'
                f'oznaka: "{esc(oznaka)}"\n'
                f'vrsta: "{esc(vrsta)}"\n'
                f'status: "{esc(status)}"\n'
                f'mandat: {mandat}\n'
                f'zbirka: "Seje {prefix}"\n'
                "---\n"
            )
            body = f"# Seja {oznaka} ({vrsta})\n\n"
            body += f"**Status:** {status}  \n**Mandat:** {mandat}  \n\n"

            dz = item.find("DOBESEDNI_ZAPISI_SEJE")
            if dz is not None:
                dzids = [u.text.strip().split("|")[-1].strip()
                         for u in dz.findall("UNID") if u.text]
                if dzids:
                    body += "## Dobesedni zapisi\n\n"
                    for d in dzids:
                        body += f"- {d}\n"

            if not dry_run:
                (out / f"{prefix}-{safe(unid)}.md").write_text(fm + body, encoding="utf-8")
                save_progress(prefix, item_id)
            ok += 1

    print(f"{prefix} total: {ok} written, {skip} skipped")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run",  action="store_true")
    parser.add_argument("--skip-ul",  action="store_true", help="Don't fetch UL text for PZ items")
    parser.add_argument("--workers",  type=int, default=6)
    parser.add_argument("--only",     help="Only process: VPP,PZ,GDZ,GDT,SDT,SDZ (comma-separated)")
    args = parser.parse_args()

    OUT_DIR.mkdir(exist_ok=True)
    only = set(args.only.upper().split(",")) if args.only else {"VPP", "PZ", "GDZ", "GDT", "SDT", "SDZ"}

    print("=== DZ Open Data Fetcher (all mandates) ===")
    print(f"Output: {OUT_DIR} | Workers: {args.workers} | Dry-run: {args.dry_run}\n")

    if "VPP" in only:
        process_vpp(load_progress("VPP"), args.dry_run)

    if "PZ" in only:
        process_pz(load_progress("PZ"), args.dry_run, not args.skip_ul, args.workers)

    if "GDZ" in only:
        process_voting("GDZ", load_progress("GDZ"), args.dry_run)

    if "GDT" in only:
        process_voting("GDT", load_progress("GDT"), args.dry_run)

    if "SDT" in only:
        process_sessions("SDT", load_progress("SDT"), args.dry_run)

    if "SDZ" in only:
        process_sessions("SDZ", load_progress("SDZ"), args.dry_run)

    print("\n=== Done. Files in dz/ — no git commits made. ===")
    print("Commit with: git add dz/ us_rs/ && git commit -m 'Add DZ open data and Constitutional Court decisions'")


if __name__ == "__main__":
    main()
