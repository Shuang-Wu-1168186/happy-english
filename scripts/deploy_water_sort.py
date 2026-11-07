"""Deploy only the water-sort release, with drift checks and code rollback.

Run from the backend project after tests pass. No .env, credentials, unrelated
working-tree files, static uploads or textbook data are uploaded.
"""

import hashlib
import json
from pathlib import Path
import shlex
import subprocess
import tarfile
import tempfile
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
HOST = "root@147.139.172.68"
APP = "/home/admin/happy_english_server/happy-english"
BASELINE = {
    "app/main.py": "d7c64d6296208929d9ca7cc768dfa404390c5478c18333a72ab1e7c2c78fe000",
    "app/models.py": "47f80b4698928634ee9c042b6b5c44194be056d28596c8e1a17d2cd569661272",
    "app/dao/__init__.py": "0d0f1431230d4d997c344ac3945ebf4d0570cf2176144f7221f4c020e546b972",
    "app/services/registry.py": "97f9ac5da86c979f7360e6e125b7813f4d2c3e0540c1f7affad673f9b2fb3903",
    "app/api/opaque_ids.py": "ab25b75ad3993e59f62ca14f1efd0b2da3196f681054c0afa1983fc3d17dcd80",
    "app/dao/water_sort.py": "f9cd3dbb78628c28d75bc2d1c897fa3c1c59d5624264b9cf885424920a83f6d4",
    "app/api/water_sort.py": "45142e0210ffb731f4bab8ce0dcff841d318fbf3732825739419ec0e701186bf",
    "app/services/water_sort.py": "ca92cf5dacc67fdebbcb890d52d1703caac01a0342f959644858164d68b3fcfa",
    "app/services/water_sort_catalog.py": "1c85afbb870c09bd48d1579ff873d692cc01e3321f36206a8d923e8c4b2540d0",
    "app/data/water_sort/campaign-200.json": "9a8e7280a1296a07789591ba31bcb23fbedc970f2bf9413561eeccbaec99d165",
}
FILES = list(BASELINE) + [
    "app/data/water_sort/campaign-810-v7.json",
    "app/data/water_sort/translations.json", "app/data/water_sort/ECDICT-LICENSE.txt",
    "sql/20261105_add_water_sort_game.sql",
]


def main():
    stage = "/tmp/happylingo-water-sort-" + uuid4().hex
    with tempfile.TemporaryDirectory(prefix="water-sort-release-") as temporary:
        directory = Path(temporary)
        metadata = {"baseline": BASELINE, "files": {f: hashlib.sha256((ROOT / f).read_bytes()).hexdigest() for f in FILES}}
        (directory / "release.json").write_text(json.dumps(metadata, indent=2))
        archive = directory / "release.tar.gz"
        with tarfile.open(archive, "w:gz") as package:
            for file in FILES:
                package.add(ROOT / file, arcname=file)
            package.add(directory / "release.json", arcname="release.json")
            package.add(ROOT / "scripts/install_water_sort_release.py", arcname="install.py")
        subprocess.run(["ssh", "-o", "BatchMode=yes", HOST, "mkdir -m 700 " + shlex.quote(stage)], check=True)
        subprocess.run(["scp", "-q", str(archive), HOST + ":" + stage + "/release.tar.gz"], check=True)
        command = (f"tar -xzf {shlex.quote(stage + '/release.tar.gz')} -C {shlex.quote(stage)} && "
                   f"{shlex.quote(APP + '/venv/bin/python')} {shlex.quote(stage + '/install.py')} {shlex.quote(stage)} {shlex.quote(APP)}")
        subprocess.run(["ssh", "-o", "BatchMode=yes", HOST, command], check=True)


if __name__ == "__main__":
    main()
