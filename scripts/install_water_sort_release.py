"""Executed by deploy_water_sort.py on the existing Aliyun host."""

import ast
from datetime import datetime, UTC
import hashlib
import json
import os
from pathlib import Path
import pwd
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    stage, app = map(Path, sys.argv[1:3])
    release = json.loads((stage / "release.json").read_text())
    files = release["files"]
    for name, digest in files.items():
        if sha(stage / name) != digest:
            raise RuntimeError("Invalid release checksum: " + name)
        if name.endswith(".py"):
            ast.parse((stage / name).read_text())
        target = app / name
        if target.exists() and sha(target) not in {digest, release["baseline"].get(name)}:
            raise RuntimeError("Server file changed since preflight: " + name)
    backup = app.parent / "backups" / ("water-sort-" + datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ"))
    backup.mkdir(parents=True, mode=0o700)
    present = []
    for name in files:
        if (app / name).exists():
            target = backup / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(app / name, target)
            present.append(name)
    (backup / "release.json").write_text(json.dumps({**release, "previously_present": present}, indent=2))
    python = str(app / "venv/bin/python")
    account = pwd.getpwnam("admin")
    try:
        # Publish dependencies before router registration. The running worker
        # keeps the previous imported application until the controlled restart.
        for name in sorted(files, key=lambda value: value == "app/main.py"):
            target = app / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(stage / name, target)
            os.chown(target, account.pw_uid, account.pw_gid)
        sys.path.insert(0, str(app))
        from app.core.config import Settings
        from app.core.database import make_engine
        from sqlalchemy import text
        engine = make_engine(Settings().database_url)
        sql = (stage / "sql/20261105_add_water_sort_game.sql").read_text()
        sql = "\n".join(line for line in sql.splitlines() if not line.lstrip().startswith("--"))
        with engine.begin() as connection:
            for statement in sql.split(";"):
                if statement.strip():
                    connection.execute(text(statement))
        preflight = """
from app.main import create_app
from app.services.water_sort_catalog import WaterSortCatalog, manifest
from sqlalchemy.orm import Session
from collections import Counter
app = create_app()
with Session(app.state.engine) as db:
    catalog = WaterSortCatalog(db, {'id': 0, 'role': 'admin'})
    assert set(w['book'] for w in catalog.words) == set(range(1, 13))
    assert len(manifest()) == 810
    assert all(b['word_id'] in catalog.by_id for l in manifest() for b in l['bottles'])
    print('PREFLIGHT_WORDS', len(catalog.words), dict(sorted(Counter(w['book'] for w in catalog.words).items())))
"""
        subprocess.run([python, "-c", preflight], cwd=app, check=True)
        subprocess.run(["systemctl", "restart", "happy_english"], check=True)
        ready = False
        for _ in range(30):
            try:
                with urllib.request.urlopen("http://127.0.0.1:8000/api/health/ready", timeout=2) as response:
                    ready = response.status == 200
                if ready:
                    break
            except (OSError, urllib.error.URLError):
                time.sleep(0.5)
        if not ready:
            raise RuntimeError("Readiness check failed")
        try:
            urllib.request.urlopen("http://127.0.0.1:8000/api/game/v1/water-sort/progress", timeout=5)
            raise RuntimeError("Game progress must require authentication")
        except urllib.error.HTTPError as error:
            if error.code != 401:
                raise
        print("DEPLOYED", "https://api.happylingo.cn/api/game/v1/water-sort", "BACKUP", backup)
    except Exception:
        for name in files:
            target = app / name
            if name in present:
                shutil.copy2(backup / name, target)
                os.chown(target, account.pw_uid, account.pw_gid)
            else:
                target.unlink(missing_ok=True)
        subprocess.run(["systemctl", "restart", "happy_english"], check=False)
        # The additive game tables remain; no existing table or user data is removed.
        print("CODE_ROLLED_BACK", backup)
        raise


if __name__ == "__main__":
    main()
