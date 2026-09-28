# Teams for Linux COPR packaging

This repository repackages the official Teams for Linux RPM for Fedora COPR.
It does not build Teams for Linux from source. The spec downloads the exact
upstream release asset and verifies its SHA-256 checksum before extracting its
payload.

## Update procedure

1. Obtain the current x86_64 RPM's version, download URL, and SHA-256 digest
   from [Teams for Linux releases](https://github.com/IsmaelMartinez/teams-for-linux/releases).
2. Update `Version`, `Release`, the `Source0` URL, the checksum in
   `teams-for-linux.spec`, and `source_url` in `.copr/Makefile`.
3. Build from SCM in COPR for Fedora 43, 44, 45, and Rawhide on x86_64.

Install the resulting package with:

```bash
sudo dnf copr enable ok8219/teams-for-linux
sudo dnf install teams-for-linux
```
