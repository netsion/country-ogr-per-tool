#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Upload minio-store/ images to MinIO via S3 SigV4 (pure stdlib, no deps).

Works on Python >= 3.6 (production-verified target: 3.6.8, Linux).

Kit layout (this script at kit root):
  upload_to_minio.py     <- this file (single-file, stdlib only)
  minio-store/default/   <- images; object key = path below default/
  minio.conf             <- optional config KEY=VALUE (env vars override)

Object key equals dataset profile.minio_path; bucket default: "default".

Usage:
  python3 upload_to_minio.py --selftest   # offline SigV4 vector check
  python3 upload_to_minio.py --dry        # list manifest
  python3 upload_to_minio.py              # upload (resumable, 4 threads)
  python3 upload_to_minio.py --verify     # HEAD every key, compare size
"""
import glob
import hashlib
import hmac
import http.client
import json
import os
import ssl
import sys
import time
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

KIT = os.path.dirname(os.path.abspath(__file__))
STORE = os.path.join(KIT, "minio-store", "default")
STATE = os.path.join(KIT, "upload_state.json")
CONF = os.path.join(KIT, "minio.conf")

CONTENT_TYPES = {
    ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
    ".gif": "image/gif", ".webp": "image/webp", ".svg": "image/svg+xml",
    ".tif": "image/tiff", ".tiff": "image/tiff", ".bmp": "image/bmp",
    ".ico": "image/x-icon", ".avif": "image/avif",
}


def cfg(name, default=None):
    v = os.environ.get(name)
    if v:
        return v
    if os.path.exists(CONF):
        for line in open(CONF, encoding="utf-8"):
            line = line.strip()
            if line.startswith("#") or "=" not in line:
                continue
            k, val = line.split("=", 1)
            if k.strip() == name:
                return val.strip()
    return default


# ---------------- S3 SigV4 (pure stdlib) ----------------

def _uri_encode_path(key):
    """S3 canonical URI: each path segment RFC3986-encoded, '/' kept."""
    return "/".join(urllib.parse.quote(seg, safe="") for seg in key.split("/"))


def sigv4_headers(method, canonical_uri, headers, payload, region,
                  access_key, secret_key):
    """Return {Authorization: ...} adding to given headers (dict, lowercase).

    headers must already include host / x-amz-date / x-amz-content-sha256
    (and any extra signed headers like content-type). All keys lowercase.
    """
    signed_names = ";".join(sorted(headers.keys()))
    canonical_headers = "".join(
        "%s:%s\n" % (k, headers[k]) for k in sorted(headers.keys()))
    creq = "\n".join([method, canonical_uri, "",
                      canonical_headers, signed_names, payload])
    amz_date = headers["x-amz-date"]
    scope = "%s/%s/s3/aws4_request" % (amz_date[:8], region)
    sts = "\n".join(["AWS4-HMAC-SHA256", amz_date, scope,
                     hashlib.sha256(creq.encode("utf-8")).hexdigest()])

    def _h(key, msg):
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

    k = _h(("AWS4" + secret_key).encode("utf-8"), amz_date[:8])
    k = _h(k, region)
    k = _h(k, "s3")
    k = _h(k, "aws4_request")
    sig = hmac.new(k, sts.encode("utf-8"), hashlib.sha256).hexdigest()
    auth = ("AWS4-HMAC-SHA256 Credential=%s/%s, SignedHeaders=%s, Signature=%s"
            % (access_key, scope, signed_names, sig))
    out = {k: headers[k] for k in headers}
    out["authorization"] = auth
    return out


class S3Client(object):
    def __init__(self, endpoint, access_key, secret_key, region="us-east-1",
                 secure=True, insecure_tls=False, bucket="default"):
        host, _, port = endpoint.partition(":")
        self.host, self.port = host, (int(port) if port else (443 if secure else 80))
        self.ak, self.sk, self.region = access_key, secret_key, region
        self.secure, self.insecure_tls, self.bucket = secure, insecure_tls, bucket

    def _conn(self):
        if self.secure:
            ctx = ssl.create_default_context()
            if self.insecure_tls:
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
            return http.client.HTTPSConnection(self.host, self.port, context=ctx, timeout=120)
        return http.client.HTTPConnection(self.host, self.port, timeout=120)

    def request(self, method, key, body=b"", extra_headers=None,
                expect=(200, 201, 204, 206)):
        path = "/%s/%s" % (self.bucket, _uri_encode_path(key))
        payload = hashlib.sha256(body).hexdigest()
        amz_date = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
        hosthdr = self.host if self.port in (80, 443) else "%s:%d" % (self.host, self.port)
        headers = {
            "host": hosthdr,
            "x-amz-date": amz_date,
            "x-amz-content-sha256": payload,
        }
        if body or extra_headers and "content-type" in extra_headers:
            pass
        if extra_headers:
            headers.update({k.lower(): v for k, v in extra_headers.items()})
        signed = sigv4_headers(method, path, headers, payload,
                               self.region, self.ak, self.sk)
        conn = self._conn()
        conn.request(method, path, body=body, headers=signed)
        resp = conn.getresponse()
        data = resp.read()
        status = resp.status
        conn.close()
        if status not in expect:
            raise RuntimeError("HTTP %s for %s %s: %s"
                               % (status, method, key, data[:200]))
        return resp, data

    def put_file(self, key, filepath, content_type):
        with open(filepath, "rb") as fh:
            body = fh.read()
        self.request("PUT", key, body=body,
                     extra_headers={"content-type": content_type})

    def head(self, key):
        resp, _ = self.request("HEAD", key, body=b"", expect=(200,))
        return int(resp.getheader("Content-Length", "0"))


def selftest():
    """AWS SigV4 official test vector (S3 GET object example)."""
    headers = {
        "host": "examplebucket.s3.amazonaws.com",
        "range": "bytes=0-9",
        "x-amz-content-sha256":
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "x-amz-date": "20130524T000000Z",
    }
    payload = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    out = sigv4_headers("GET", "/test.txt", headers, payload,
                        "us-east-1", "AKIAIOSFODNN7EXAMPLE",
                        "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY")
    want = ("AWS4-HMAC-SHA256 "
            "Credential=AKIAIOSFODNN7EXAMPLE/20130524/us-east-1/s3/aws4_request, "
            "SignedHeaders=host;range;x-amz-content-sha256;x-amz-date, "
            "Signature=f0e8bdb87c964420e857bd35b5d6ed310bd44f0170aba48dd91039c6036bdb41")
    got = out["authorization"].replace("SignedHeaders=host;range;",
                                        "SignedHeaders=host;range;")
    ok = got == want
    print("selftest:", "PASS" if ok else "FAIL")
    if not ok:
        print("want:", want)
        print("got :", got)
    return ok


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


def load_state():
    if os.path.exists(STATE):
        with open(STATE, encoding="utf-8") as fh:
            return set(json.load(fh)["done"])
    return set()


def save_state(done):
    tmp = STATE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump({"done": sorted(done)}, fh)
    os.replace(tmp, STATE)


def main():
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    mode = "verify" if "--verify" in sys.argv else ("dry" if "--dry" in sys.argv else "upload")
    bucket = cfg("MINIO_BUCKET", "default")
    manifest = build_manifest()
    total_mb = sum(m["size"] for m in manifest) / 1024 / 1024
    print("manifest: %d objects, %.0f MB total, bucket=%s" % (len(manifest), total_mb, bucket))
    if mode == "dry":
        for m in manifest[:10]:
            print("  %s  (%dB %s)" % (m["key"], m["size"], m["ct"]))
        return

    endpoint = cfg("MINIO_ENDPOINT", "") or ""
    endpoint = endpoint.strip().rstrip("/")
    secure_val = cfg("MINIO_SECURE")
    if endpoint.lower().startswith("https://"):
        endpoint = endpoint[8:]
        secure = True if secure_val is None else \
            str(secure_val).lower() not in ("0", "false", "no")
    elif endpoint.lower().startswith("http://"):
        endpoint = endpoint[7:]
        secure = False if secure_val is None else \
            str(secure_val).lower() not in ("0", "false", "no")
    else:
        secure = str(secure_val or "1").lower() not in ("0", "false", "no")
    if not endpoint:
        sys.exit("MINIO_ENDPOINT not set (env or minio.conf)")
    client = S3Client(endpoint, cfg("MINIO_ACCESS_KEY", ""), cfg("MINIO_SECRET_KEY", ""),
                      region=cfg("MINIO_REGION", "us-east-1"), secure=secure,
                      insecure_tls=str(cfg("MINIO_INSECURE", "0")).lower() in ("1", "true"),
                      bucket=bucket)
    # connectivity check: HEAD bucket (404/403 acceptable errors prove reachability)
    try:
        client.request("HEAD", "", body=b"", expect=(200, 204, 301, 403, 404))
        print("bucket '%s' reachable" % bucket)
    except Exception as e:
        print("WARNING: bucket check: %s (continuing)" % str(e)[:120])

    if mode == "verify":
        ok = miss = bad = 0
        for i, m in enumerate(manifest, 1):
            try:
                rsize = client.head(m["key"])
                if rsize == m["size"]:
                    ok += 1
                else:
                    bad += 1
                    print("  SIZE-DIFF %s local=%d remote=%d" % (m["key"], m["size"], rsize))
            except Exception:
                miss += 1
                if miss <= 10:
                    print("  MISSING %s" % m["key"])
            if i % 1000 == 0:
                print("  ... %d/%d" % (i, len(manifest)), flush=True)
        print("verify: ok=%d missing=%d size-diff=%d / %d" % (ok, miss, bad, len(manifest)))
        return

    done = load_state()
    todo = [m for m in manifest if m["key"] not in done]
    print("todo: %d (already uploaded: %d)" % (len(todo), len(done)))
    t0 = time.time()
    n = fail = 0

    def upload_one(m):
        last = None
        for i in range(3):
            try:
                client.put_file(m["key"], m["abs"], m["ct"])
                return m["key"], None
            except Exception as e:
                last = e
                time.sleep(2 + i * 3)
        return m["key"], str(last)[:150]

    with ThreadPoolExecutor(max_workers=4) as ex:
        futs = [ex.submit(upload_one, m) for m in todo]
        for fut in as_completed(futs):
            key, err = fut.result()
            n += 1
            if err:
                fail += 1
                print("FAIL %s: %s" % (key, err))
            else:
                done.add(key)
            if n % 100 == 0:
                save_state(done)
                rate = n / (time.time() - t0) * 60
                print("[ckpt] %d/%d fail=%d %.0f/min eta=%.0fmin"
                      % (n, len(todo), fail, rate, (len(todo) - n) / rate), flush=True)
    save_state(done)
    print("DONE uploaded=%d fail=%d elapsed=%.0fs" % (len(done), fail, time.time() - t0))


if __name__ == "__main__":
    main()
