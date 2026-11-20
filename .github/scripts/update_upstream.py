#!/usr/bin/env python3
"""Prepare a packaging PR for the latest stable Teams for Linux release."""

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
API_URL = "https://api.github.com/repos/IsmaelMartinez/teams-for-linux/releases/latest"
ASSET_BASE = "https://github.com/IsmaelMartinez/teams-for-linux/releases/download/"


def get(url):
    return urlopen(Request(url, headers={"User-Agent": "teams-for-linux-copr-release-check"}), timeout=180)


def replace_once(text, pattern, replacement, label):
    result, count = re.subn(pattern, replacement, text, count=1, flags=re.MULTILINE)
    if count != 1:
        raise ValueError(f"Expected one {label}; found {count}")
    return result


def main():
    with get(API_URL) as response:
        release = json.load(response)
    if release.get("draft") or release.get("prerelease"):
        raise ValueError("Latest release is not stable")
    version = release.get("tag_name", "").removeprefix("v")
    if not re.fullmatch(r"\d+(?:\.\d+)+", version):
        raise ValueError(f"Unexpected release tag: {release.get('tag_name')}")

    spec_path = ROOT / "teams-for-linux.spec"
    makefile_path = ROOT / ".copr/Makefile"
    spec, makefile = spec_path.read_text(), makefile_path.read_text()
    current_match = re.search(r"^Version:\s+(\S+)$", spec, re.MULTILINE)
    if not current_match:
        raise ValueError("Could not read Teams for Linux package version")
    current = current_match.group(1)
    if tuple(map(int, version.split("."))) <= tuple(map(int, current.split("."))):
        print("updated=false")
        print(f"version={current}")
        print(f"release_url={release.get('html_url', '')}")
        return

    name = f"teams-for-linux-{version}.x86_64.rpm"
    assets = {asset.get("name"): asset.get("browser_download_url") for asset in release.get("assets", [])}
    url = assets.get(name)
    if not url or not url.startswith(ASSET_BASE):
        raise ValueError(f"Release is missing expected RPM asset {name}")
    digest = hashlib.sha256()
    with get(url) as response:
        while chunk := response.read(1024 * 1024):
            digest.update(chunk)

    spec = replace_once(spec, r"^(Version:\s+)\S+$", rf"\g<1>{version}", "Version")
    spec = replace_once(
        spec,
        r'^(echo ")[0-9a-f]{64}(  %\{SOURCE0\}" \| sha256sum --check)$',
        rf"\g<1>{digest.hexdigest()}\g<2>",
        "source checksum",
    )
    spec = replace_once(spec, r"^(Release:\s+)\S+$", r"\g<1>1%{?dist}", "Release")
    makefile = replace_once(makefile, r"^(version := )\S+$", rf"\g<1>{version}", "COPR version")

    date = datetime.now(timezone.utc).strftime("%a %b %d %Y")
    entry = f"* {date} OK <4374115+kappa8219@users.noreply.github.com> - {version}-1\n- Update to Teams for Linux {version}\n\n"
    spec = replace_once(spec, r"^%changelog[ \t]*\n", "%changelog\n" + entry, "changelog")
    spec_path.write_text(spec)
    makefile_path.write_text(makefile)
    print("updated=true")
    print(f"version={version}")
    print(f"release_url={release.get('html_url', '')}")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Release update failed: {error}", file=sys.stderr)
        sys.exit(1)
