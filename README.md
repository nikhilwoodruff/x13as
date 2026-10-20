# x13as

The US Census Bureau's [X-13ARIMA-SEATS](https://www.census.gov/data/software/x13as.X-13ARIMA-SEATS.html) seasonal adjustment program (the engine ONS uses, typically in X-11 mode), compiled and bundled as a Python wheel. Census publishes Linux and Windows binaries only; this builds from their Fortran source, so it also works on macOS arm64.

```python
import x13as

x13as.binary_path()          # path to the bundled executable
res = x13as.x13_arima_analysis(series, outlier=True)   # needs the [statsmodels] extra
res.seasadj, res.trend
```

The `x13as` command passes straight through to the binary, so `x13as myspec` runs a hand-written `myspec.spc`.

Wheels: macOS arm64 (11+), and Linux x86_64 and aarch64. The Linux binary is fully static, so it runs on any glibc or musl distribution.

## Building

```sh
# macOS
micromamba create -n x13build -c conda-forge gfortran make
micromamba run -n x13build ./scripts/build_binary.sh   # writes src/x13as/_bin/x13as
uv build --wheel

# Linux (in Docker; builds, then tests the wheel)
./scripts/build_linux.sh            # amd64 and arm64
```

CI (`.github/workflows/wheels.yml`) builds all three wheels on native runners and publishes to PyPI on `v*` tags via trusted publishing.

The package version tracks the Census release (1.1.62 = v1.1 build 62). X-13ARIMA-SEATS is public-domain US government software.
