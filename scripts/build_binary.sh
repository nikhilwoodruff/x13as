#!/usr/bin/env bash
# Compile the Census X-13ARIMA-SEATS ASCII build into src/x13as/_bin/x13as.
# Needs gfortran + make on PATH, e.g.
#   micromamba create -n x13build -c conda-forge gfortran make
#   micromamba run -n x13build ./scripts/build_binary.sh
set -euo pipefail

BUILD="${X13_BUILD:-62}"
SHA256_B62="82796c84b54891474df1a6ffb16be7bf7bd4a992e3679158645c888e6cddda12"
URL="https://www2.census.gov/software/x-13arima-seats/x13as/unix-linux/program-archives/x13as_asciisrc-v1-1-b${BUILD}.tar.gz"

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

curl -sSfL "$URL" -o "$WORK/src.tar.gz"
if [[ "$BUILD" == "62" ]]; then
  SHA="$(command -v sha256sum || echo "shasum -a 256")"
  echo "$SHA256_B62  $WORK/src.tar.gz" | $SHA -c -
fi
tar xzf "$WORK/src.tar.gz" -C "$WORK"
cd "$WORK"/x13as_asciisrc-v1-1-b"$BUILD"

if [[ "$(uname)" == "Darwin" ]]; then
  # macOS has no fully static linking; link the Fortran runtime statically instead.
  export MACOSX_DEPLOYMENT_TARGET="${MACOSX_DEPLOYMENT_TARGET:-11.0}"
  sed 's/-static//' makefile.gf > makefile.build
  LDFLAGS="-static-libgfortran -static-libquadmath -static-libgcc"
else
  # Fully static, like Census's own Linux build, so the wheel runs on any glibc/musl.
  cp makefile.gf makefile.build
  LDFLAGS="-s"
fi

make -f makefile.build -j"$(getconf _NPROCESSORS_ONLN)" FFLAGS="-O2 -std=legacy" LDFLAGS="$LDFLAGS"

mkdir -p "$ROOT/src/x13as/_bin"
install -m 755 x13as_ascii "$ROOT/src/x13as/_bin/x13as"
echo "$BUILD" > "$ROOT/src/x13as/_bin/BUILD"
echo "Built $ROOT/src/x13as/_bin/x13as (build $BUILD)"
