#!/usr/bin/env bash
# Build Linux wheels in Docker. Usage: scripts/build_linux.sh [amd64|arm64 ...] (default: both)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$ROOT/dist"
if [[ $# -gt 0 ]]; then ARCHES=("$@"); else ARCHES=(amd64 arm64); fi

for arch in "${ARCHES[@]}"; do
  # Repo is copied in, not mounted, so the host's macOS binary in src/x13as/_bin is untouched.
  docker run --rm --platform "linux/$arch" \
    -v "$ROOT":/src:ro -v "$ROOT/dist":/out \
    debian:bookworm-slim bash -euc '
      apt-get update -qq && apt-get install -y -qq gfortran make curl ca-certificates >/dev/null
      curl -LsSf https://astral.sh/uv/install.sh | env UV_UNMANAGED_INSTALL=/usr/local/bin sh >/dev/null
      cp -r /src /build && cd /build && rm -rf src/x13as/_bin dist
      ./scripts/build_binary.sh
      uv build --wheel --out-dir /out
      uv run --isolated --no-project --with "$(ls /out/x13as-*manylinux*$(uname -m).whl)" --with pytest \
        python -m pytest -q tests
    '
done
