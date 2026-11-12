# -*- coding: utf-8 -*-
"""Upload minio-store/ images to MinIO object storage.

Manifest  : files under minio-store/default/**  (bucket = default)
Object key: <folder>/<cc>/<ID>.<ext>            (exactly equals profile.minio_path)
Features  : resume via state file, per-file retry, Content-Type by extension,
            4 threads, progress report, --verify mode (stat all keys).
Config (env):
  MINIO_ENDPOINT   host:port, NO scheme, e.g. "play.min.io" or "10.1.2.3:9000"
  MINIO_ACCESS_KEY / MINIO_SECRET_KEY
  MINIO_SECURE     1 (https, default) / 0 (http)
  MINIO_BUCKET     default: "default"
Usage:
  python upload_to_minio.py            # upload (resumable)
  python upload_to_minio.py --verify   # stat every key, compare size
  python upload_to_minio.py --dry      # list manifest only
"""
import glob
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding="utf-8")

ROOT = "D:/ai-workspace/apec-osint-tool"
STORE = os.path.join(ROOT, "minio-store", "default")
STATE = os.path.join(ROOT, "output", "_avatar_audit", "minio_upload_state.json")
BUCKET = os.environ.get("MINIO_BUCKET", "default")

CONTENT_TYPES = {
    ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
    ".gif": "image/gif", ".webp": "image/webp", ".svg": "image/svg+xml",
    ".tif": "image/tiff", ".tiff": "image/tiff", ".bmp": "image/bmp",
    ".ico": "image/x-icon", ".avif": "image/avif",
}


def build_manifest():
    items = []
    for f in sorted(glob.glob(os.path.join(STORE, "**", "*.*"), recursive=True)):
        if not os.path.isfile(f):
            continue
        key = os.path.relpath(f, STORE).replace("\\", "/")
        items.append({"abs": f, "key": key, "size": os.path.getsize(f),
                      "ct": CONTENT_TYPES.get(os.path.splitext(f)[1].lower(),
                                              "application/octet-stream")})
    return items


def get_client():
    from minio import Minio  # pip install minio
    endpoint = os.environ.get("MINIO_ENDPOINT")
    if not endpoint:
        sys.exit("MINIO_ENDPOINT env not set (host:port, no scheme)")
    secure = os.environ.get("MINIO_SECURE", "1").lower() not in ("0", "false", "no")
    return Minio(endpoint,
                 access_key=os.environ.get("MINIO_ACCESS_KEY", ""),
                 secret_key=os.environ.get("MINIO_SECRET_KEY", ""),
                 secure=secure)


def load_state():
    if os.path.exists(STATE):
        return set(json.load(open(STATE, encoding="utf-8"))["done"])
    return set()


def save_state(done):
    tmp = STATE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump({"done": sorted(done)}, fh)
    os.replace(tmp, STATE)


def main():
    mode = "verify" if "--verify" in sys.argv else ("dry" if "--dry" in sys.argv else "upload")
    manifest = build_manifest()
    print(f"manifest: {len(manifest)} objects, "
          f"{sum(m['size'] for m in manifest)/1024/1024:.0f} MB total, bucket={BUCKET}")
    if mode == "dry":
        for m in manifest[:10]:
            print(f"  {m['key']}  ({m['size']}B {m['ct']})")
        return

    client = get_client()
    if not client.bucket_exists(BUCKET):
        sys.exit(f"bucket '{BUCKET}' does not exist (or no permission)")
    print(f"bucket '{BUCKET}' reachable")

    if mode == "verify":
        bad = miss = ok = 0
        for m in manifest:
            try:
                st = client.stat_object(BUCKET, m["key"])
                if st.size == m["size"]:
                    ok += 1
                else:
                    bad += 1
                    print(f"  SIZE-DIFF {m['key']} local={m['size']} remote={st.size}")
            except Exception:
                miss += 1
                if miss <= 10:
                    print(f"  MISSING {m['key']}")
        print(f"verify: ok={ok} missing={miss} size-diff={bad} / {len(manifest)}")
        return

    # upload mode
    done = load_state()
    todo = [m for m in manifest if m["key"] not in done]
    print(f"todo: {len(todo)} (already uploaded: {len(done)})")
    t0 = time.time()
    n = fail = 0

    def upload_one(m):
        last = None
        for i in range(3):
            try:
                client.fput_object(BUCKET, m["key"], m["abs"],
                                   content_type=m["ct"], metadata={"x-upload-src": "osint-avatar"})
                return m["key"], None
            except Exception as e:
                last = e
                time.sleep(2 + i * 3)
        return m["key"], str(last)[:120]

    with ThreadPoolExecutor(max_workers=4) as ex:
        futs = {ex.submit(upload_one, m): m for m in todo}
        for fut in as_completed(futs):
            key, err = fut.result()
            n += 1
            if err:
                fail += 1
                print(f"FAIL {key}: {err}")
            else:
                done.add(key)
            if n % 100 == 0:
                save_state(done)
                rate = n / (time.time() - t0) * 60
                print(f"[ckpt] {n}/{len(todo)} fail={fail} {rate:.0f}/min "
                      f"eta={(len(todo)-n)/rate:.0f}min", flush=True)
    save_state(done)
    print(f"DONE uploaded={len(done)} fail={fail} elapsed={(time.time()-t0):.0f}s")


if __name__ == "__main__":
    main()
