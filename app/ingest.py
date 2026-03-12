import asyncio
import json
import os
import re
from datetime import datetime, date
from pathlib import Path
from typing import Any, Dict, List, Optional

from sqlalchemy import insert

_SCRIPT_DIR = Path(__file__).resolve().parent.parent
CHUNKS_DIR: Path = Path(_SCRIPT_DIR / "nvdcpe-2.0" / "nvdcpe-2.0-chunks")

BATCH_SIZE = 500

_CPE23_RE = re.compile(r"^cpe:2\.3:([^:]+):([^:]+):([^:]+):([^:]+):.*$")


def cpe23_to_cpe22(cpe23: str) -> Optional[str]:
    """cpe:2.3:a:vendor:product:1.0:... → cpe:/a:vendor:product:1.0"""
    m = _CPE23_RE.match(cpe23)
    if not m:
        return None
    part, vendor, product, version = m.groups()
    parts_22 = [p for p in [part, vendor, product, version] if p and p != "*"]
    return "cpe:/" + ":".join(parts_22)


def _parse_dt(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    for fmt in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(value[:26], fmt)
        except ValueError:
            continue
    return None


def _parse_date(value: Optional[str]) -> Optional[date]:
    dt = _parse_dt(value)
    return dt.date() if dt else None


def _build_row(cpe_obj: Dict[str, Any]) -> Dict[str, Any]:
    cpe23_uri: str = cpe_obj.get("cpeName", "")
    cpe22_uri: Optional[str] = cpe23_to_cpe22(cpe23_uri)

    titles: list = cpe_obj.get("titles", [])
    title = None
    for t in titles:
        if t.get("lang", "").lower().startswith("en"):
            title = t.get("title")
            break
    if title is None and titles:
        title = titles[0].get("title")

    refs: list = cpe_obj.get("refs", [])
    ref_links = [r["ref"] for r in refs if r.get("ref")] or None

    deprecated: bool = cpe_obj.get("deprecated", False)
    dep_date = _parse_date(cpe_obj.get("lastModified")) if deprecated else None

    return {
        "cpe_title": title,
        "cpe_22_uri": cpe22_uri,
        "cpe_23_uri": cpe23_uri,
        "reference_links": ref_links,
        "cpe_22_deprecation_date": dep_date,
        "cpe_23_deprecation_date": dep_date,
    }


async def _ingest(chunks_dir: Path) -> None:
    from app.database import engine, Base
    from app.models import CPE

    chunk_files = sorted(chunks_dir.glob("*.json"))
    if not chunk_files:
        print(f"No JSON chunk files found in {chunks_dir}")
        return

    print(f"Found {len(chunk_files)} chunk file(s)")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    total_inserted = 0
    for chunk_path in chunk_files:
        print(f"Processing {chunk_path.name} ...", flush=True)

        with open(chunk_path, encoding="utf-8") as fp:
            data = json.load(fp)

        rows: List[Dict[str, Any]] = []
        for product in data.get("products", []):
            cpe_obj = product.get("cpe", {})
            if cpe_obj:
                rows.append(_build_row(cpe_obj))

        async with engine.begin() as conn:
            for i in range(0, len(rows), BATCH_SIZE):
                await conn.execute(insert(CPE), rows[i : i + BATCH_SIZE])

        total_inserted += len(rows)
        print(f"  done: {len(rows):,} rows from {chunk_path.name}")

    print(f"\nTotal rows inserted: {total_inserted:,}")


def main() -> None:
    asyncio.run(_ingest(CHUNKS_DIR))


if __name__ == "__main__":
    main()
