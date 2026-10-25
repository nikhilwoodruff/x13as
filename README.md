# x13as

The US Census Bureau's [X-13ARIMA-SEATS](https://www.census.gov/data/software/x13as.X-13ARIMA-SEATS.html) seasonal adjustment program (the engine ONS uses, typically in X-11 mode), compiled and bundled as a Python wheel. Census publishes Linux and Windows binaries only; this builds from their Fortran source, so it also works on macOS arm64.

## Quick start

```sh
pip install x13as
```

This installs statsmodels and pandas automatically. For example, seasonally adjust
five years of synthetic monthly sales:

```python
import numpy as np
import pandas as pd
import x13as

rng = np.random.default_rng(42)
seasonal = [80, 85, 95, 100, 105, 110, 105, 100, 95, 100, 120, 140]
sales = pd.Series(
    [seasonal[i % 12] + i * 0.5 for i in range(60)] + rng.normal(0, 3, 60),
    index=pd.date_range("2020-01-01", periods=60, freq="MS"),
)

result = x13as.x13_arima_analysis(sales, trading=False, log=False)
print(pd.DataFrame({
    "original": sales,
    "adjusted": result.seasadj,
    "trend": result.trend,
}).tail(12).round(2))
```

The random variation is part of this synthetic example; use your observed values
directly for real data. An exactly repeating seasonal pattern plus a straight-line
trend can leave no variation after differencing, which X-13 rejects with
"Differencing has annihilated the series."

`result.seasadj` contains the adjusted values and `result.trend` the trend.
`x13as.binary_path()` returns the path to the bundled executable.

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

CI (`.github/workflows/wheels.yml`) builds all three wheels on native runners,
installs each wheel into an isolated environment with only pytest added, and tests
the binary, quarterly adjustment, and the exact monthly example above. This checks
that runtime dependencies are supplied by the wheel itself. CI publishes to PyPI
on `v*` tags via trusted publishing.

The package version tracks the Census release (1.1.62 = v1.1 build 62); `.postN`
releases fix the Python packaging without changing the Census binary.
X-13ARIMA-SEATS is public-domain US government software.
