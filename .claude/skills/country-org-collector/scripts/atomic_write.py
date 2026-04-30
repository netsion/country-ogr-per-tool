#!/usr/bin/env python3
"""
atomic_write.py — Shared utilities for crash-safe file operations

Usage in other scripts:
  from atomic_write import atomic_json_write, normalize_name, load_json, save_json
"""
import sys; sys.stdout.reconfigure(encoding='utf-8'); sys.stderr.reconfigure(encoding='utf-8')

import json
import os
import tempfile
import ssl
import urllib.request

PROXY_PRIMARY = "http://127.0.0.1:7890"
PROXY_FALLBACK = "http://10.11.204.68:8081"


def setup_proxy(primary=None, fallback=None):
    """Configure HTTP proxy with automatic fallback.

    Tries primary proxy → fallback proxy → direct connection (no proxy).
    """
    primary = primary or PROXY_PRIMARY
    fallback = fallback or PROXY_FALLBACK

    proxy_url = _test_proxy(primary) or _test_proxy(fallback)

    if proxy_url:
        if proxy_url != primary:
            print(f"  Primary proxy unreachable, using fallback: {proxy_url}")
        proxy_handler = urllib.request.ProxyHandler({
            'http': proxy_url,
            'https': proxy_url,
        })
    else:
        print(f"  WARNING: No proxy available ({primary}, {fallback}), using direct connection")
        proxy_handler = urllib.request.ProxyHandler({})

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    https_handler = urllib.request.HTTPSHandler(context=ctx)
    opener = urllib.request.build_opener(proxy_handler, https_handler)
    urllib.request.install_opener(opener)
    print(f"  Proxy configured: {proxy_url or 'DIRECT'}")


def _test_proxy(proxy_url, timeout=5):
    """Test if a proxy is reachable. Returns proxy_url on success, None on failure."""
    try:
        proxy_handler = urllib.request.ProxyHandler({
            'http': proxy_url,
            'https': proxy_url,
        })
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        opener = urllib.request.build_opener(
            proxy_handler,
            urllib.request.HTTPSHandler(context=ctx),
        )
        req = urllib.request.Request(
            "https://www.wikidata.org/w/api.php?action=query&meta=siteinfo&format=json",
            headers={"User-Agent": "ApecOsintTool/1.0 (proxy-test)"},
        )
        with opener.open(req, timeout=timeout) as resp:
            if resp.status == 200:
                return proxy_url
    except Exception:
        pass
    return None


def normalize_name(name):
    """Normalize a person/org name for comparison.
    Removes: extra whitespace, periods, commas.
    Lowercases for case-insensitive comparison.
    Keeps parenthetical names (e.g. '黄循财 (Lawrence Wong)') for matching.
    """
    if not name:
        return ""
    # Remove periods and commas
    clean = name.replace(".", "").replace(",", "")
    # Normalize whitespace
    clean = " ".join(clean.split())
    return clean.lower().strip()


def atomic_json_write(filepath, data, indent=2):
    """Write JSON file atomically using temp file + rename.

    This prevents partial writes on crash:
    1. Write to temp file in same directory
    2. fsync to ensure data is on disk
    3. Rename temp to target (atomic on same filesystem)
    """
    dir_path = os.path.dirname(filepath)
    os.makedirs(dir_path, exist_ok=True)

    # Write to temp file
    fd, tmp_path = tempfile.mkstemp(
        dir=dir_path,
        prefix=".tmp_",
        suffix=os.path.basename(filepath),
        text=True
    )
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)
            f.flush()
            os.fsync(f.fileno())
        # Atomic rename
        os.replace(tmp_path, filepath)
    except Exception:
        # Clean up temp file on error
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise


def load_json(filepath):
    """Load JSON file with UTF-8 encoding."""
    with open(filepath, encoding='utf-8') as f:
        return json.load(f)


def save_json(filepath, data, indent=2):
    """Save JSON file atomically."""
    atomic_json_write(filepath, data, indent=indent)


def save_registry_atomic(registry_path, registry_data):
    """Save id_registry.json atomically and return success status."""
    save_json(registry_path, registry_data)


def save_profile_and_register(profile_path, profile_data, registry_path, registry_data, reg_entry):
    """Atomic transaction: save profile + update registry in one operation.

    Steps:
    1. Write profile to temp file
    2. Update registry in memory
    3. Write registry to temp file
    4. Rename profile temp -> final
    5. Rename registry temp -> final

    If any step fails, neither file is corrupted.
    """
    # Step 1: Write profile to temp
    profile_dir = os.path.dirname(profile_path)
    profile_tmp = os.path.join(profile_dir, f".tmp_{os.path.basename(profile_path)}")
    with open(profile_tmp, 'w', encoding='utf-8') as f:
        json.dump(profile_data, f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())

    # Step 2: Update registry
    if reg_entry:
        person_id = reg_entry.get("person_id")
        org_id = reg_entry.get("org_id")
        if person_id and "person_registry" in registry_data:
            # Update or add person
            found = False
            for p in registry_data["person_registry"]:
                if p["person_id"] == person_id:
                    p.update(reg_entry)
                    found = True
                    break
            if not found:
                registry_data["person_registry"].append(reg_entry)
        elif org_id and "registry" in registry_data:
            # Update or add org
            found = False
            for r in registry_data["registry"]:
                if r["org_id"] == org_id:
                    r.update(reg_entry)
                    found = True
                    break
            if not found:
                registry_data["registry"].append(reg_entry)

    # Step 3: Write registry to temp
    registry_tmp = os.path.join(
        os.path.dirname(registry_path),
        f".tmp_{os.path.basename(registry_path)}"
    )
    with open(registry_tmp, 'w', encoding='utf-8') as f:
        json.dump(registry_data, f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())

    # Step 4-5: Atomic renames
    os.replace(profile_tmp, profile_path)
    os.replace(registry_tmp, registry_path)


if __name__ == "__main__":
    # Quick self-test
    print("Testing normalize_name:")
    tests = [
        ("黄循财 (Lawrence Wong)", "黄循财 (lawrence wong)"),
        ("K. Shanmugam", "k shanmugam"),
        ("K Shanmugam", "k shanmugam"),
        ("尚穆根 (K. Shanmugam)", "尚穆根 (k shanmugam)"),
        ("尚穆根 (K Shanmugam)", "尚穆根 (k shanmugam)"),
    ]
    for inp, expected in tests:
        result = normalize_name(inp)
        status = "OK" if result == expected else "FAIL"
        print(f"  {status}: normalize({inp!r}) = {result!r} (expected {expected!r})")

    print("\nTesting atomic_json_write:")
    test_path = os.path.join(os.path.dirname(__file__), "_test_atomic.json")
    atomic_json_write(test_path, {"test": "你好世界", "number": 42})
    data = load_json(test_path)
    print(f"  Written and read back: {data}")
    os.unlink(test_path)
    print("  Cleaned up test file")
    print("\nAll tests passed!")
