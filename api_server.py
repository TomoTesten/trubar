#!/usr/bin/env python3
"""
T.R.U.B.A.R. REST API — serves law data from trubar.db
Run: uvicorn api_server:app --host 0.0.0.0 --port 8000
Docs: http://localhost:8000/docs
"""
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3, json
from pathlib import Path
from typing import Optional

DB_PATH = Path(__file__).parent / "trubar.db"

app = FastAPI(
    title="T.R.U.B.A.R. API",
    description="Slovenian legislation — full-text search, browse, SQL queries",
    version="1.0.0",
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET"], allow_headers=["*"])

def get_db():
    if not DB_PATH.exists():
        raise HTTPException(503, "Database not built yet. Run build_db.py first.")
    return sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)

def row_to_dict(cursor, row):
    return {d[0]: row[i] for i, d in enumerate(cursor.description)}

@app.get("/")
def root():
    return {"name": "T.R.U.B.A.R. API", "docs": "/docs", "endpoints": [
        "/search", "/law/{kratica}", "/laws", "/amendments/{kratica}", "/sql"
    ]}

@app.get("/search")
def search(
    q: str = Query(..., description="Search query"),
    vrsta: Optional[str] = Query(None, description="Filter by type: zakon, uredba, pravilnik..."),
    limit: int = Query(20, le=100),
):
    """Full-text search using FTS5."""
    db = get_db()
    try:
        if vrsta:
            rows = db.execute(
                """SELECT l.kratica, l.naziv, l.vrsta, l.datum, l.status,
                          snippet(laws_fts, 1, '[', ']', '...', 32) as excerpt
                   FROM laws_fts JOIN laws l ON l.id = laws_fts.rowid
                   WHERE laws_fts MATCH ? AND l.vrsta = ?
                   ORDER BY rank LIMIT ?""",
                (q, vrsta, limit)
            ).fetchall()
        else:
            rows = db.execute(
                """SELECT l.kratica, l.naziv, l.vrsta, l.datum, l.status,
                          snippet(laws_fts, 1, '[', ']', '...', 32) as excerpt
                   FROM laws_fts JOIN laws l ON l.id = laws_fts.rowid
                   WHERE laws_fts MATCH ?
                   ORDER BY rank LIMIT ?""",
                (q, limit)
            ).fetchall()
        cur = db.cursor()
        cur.execute("SELECT 1")  # just to get description
        # Manual column mapping
        cols = ["kratica","naziv","vrsta","datum","status","excerpt"]
        return {"results": [dict(zip(cols, r)) for r in rows], "count": len(rows)}
    finally:
        db.close()

@app.get("/law/{kratica}")
def get_law(kratica: str):
    """Get a single law by kratica."""
    db = get_db()
    try:
        row = db.execute(
            "SELECT * FROM laws WHERE kratica = ? LIMIT 1", (kratica,)
        ).fetchone()
        if not row:
            raise HTTPException(404, f"Law '{kratica}' not found")
        cols = [d[0] for d in db.execute("SELECT * FROM laws LIMIT 0").description]
        return dict(zip(cols, row))
    finally:
        db.close()

@app.get("/laws")
def list_laws(
    vrsta: Optional[str] = None,
    organ: Optional[str] = None,
    status: Optional[str] = None,
    datum_od: Optional[str] = None,
    datum_do: Optional[str] = None,
    limit: int = Query(50, le=500),
    offset: int = 0,
):
    """Browse laws with filters."""
    db = get_db()
    try:
        where, params = [], []
        if vrsta:   where.append("vrsta = ?");   params.append(vrsta)
        if organ:   where.append("organ LIKE ?"); params.append(f"%{organ}%")
        if status:  where.append("status LIKE ?");params.append(f"%{status}%")
        if datum_od:where.append("datum >= ?");   params.append(datum_od)
        if datum_do:where.append("datum <= ?");   params.append(datum_do)
        sql = "SELECT kratica, naziv, vrsta, datum, organ, status FROM laws"
        if where: sql += " WHERE " + " AND ".join(where)
        sql += " ORDER BY datum DESC LIMIT ? OFFSET ?"
        params += [limit, offset]
        rows = db.execute(sql, params).fetchall()
        cols = ["kratica","naziv","vrsta","datum","organ","status"]
        return {"results": [dict(zip(cols, r)) for r in rows], "count": len(rows), "offset": offset}
    finally:
        db.close()

@app.get("/amendments/{kratica}")
def get_amendments(kratica: str):
    """Get amendment history for a law."""
    db = get_db()
    try:
        rows = db.execute(
            "SELECT * FROM amendments WHERE kratica = ? ORDER BY datum",
            (kratica,)
        ).fetchall()
        cols = ["kratica","sprememba_kratica","sprememba_naziv","datum"]
        return {"kratica": kratica, "amendments": [dict(zip(cols, r)) for r in rows]}
    finally:
        db.close()

@app.get("/sql")
def query_sql(
    q: str = Query(..., description="SELECT query against laws and amendments tables"),
    limit: int = Query(100, le=200),
):
    """Run arbitrary read-only SQL (SELECT only)."""
    if not q.strip().upper().startswith("SELECT"):
        raise HTTPException(400, "Only SELECT queries allowed")
    db = get_db()
    try:
        cur = db.execute(q)
        cols = [d[0] for d in cur.description]
        rows = cur.fetchmany(limit)
        return {"columns": cols, "rows": [list(r) for r in rows], "count": len(rows)}
    except Exception as e:
        raise HTTPException(400, str(e))
    finally:
        db.close()
