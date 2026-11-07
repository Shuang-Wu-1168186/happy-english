"""Temporary least-privilege learner for release verification (run on the server).

Provision stdout is a credential JSON: redirect to a private file, never logs.
Cleanup removes only the generated smoke user; foreign keys remove their game data.
"""

import json
import os
from pathlib import Path
import secrets
import sys
from uuid import uuid4

from sqlalchemy import create_engine, select

from app import models as m
from app.core.config import Settings
from app.core.security import hash_password

FILE = Path("/root/water-sort-release-smoke.json")


def main():
    engine = create_engine(Settings().database_url, pool_pre_ping=True)
    if sys.argv[1] == "provision":
        if FILE.exists():
            raise SystemExit("Smoke account already provisioned; clean it up first.")
        data = {"username": "water_sort_smoke_" + uuid4().hex[:12], "password": secrets.token_urlsafe(24)}
        with engine.begin() as db:
            result = db.execute(m.user.insert().values(username=data["username"],
                password_hash=hash_password(data["password"]), full_name="Water Sort release verification",
                role="learner", status="active"))
            data["user_id"] = result.inserted_primary_key[0]
        descriptor = os.open(FILE, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, "w") as stream:
            stream.write(json.dumps(data))
        print(json.dumps(data))
    elif sys.argv[1] == "cleanup":
        data = json.loads(FILE.read_text())
        assert data["username"].startswith("water_sort_smoke_")
        with engine.begin() as db:
            user = db.execute(select(m.user).where(m.user.c.id == data["user_id"], m.user.c.username == data["username"])).mappings().one()
            assert user["role"] == "learner"
            # Retain the normal login audit trail. It has ON DELETE SET NULL.
            db.execute(m.user.delete().where(m.user.c.id == data["user_id"]))
        FILE.unlink()
        print("Temporary smoke account and game progress removed.")
    else:
        raise SystemExit("Use provision or cleanup")


if __name__ == "__main__":
    main()
