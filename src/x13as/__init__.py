import os
import stat
import sys
from importlib.resources import files
from pathlib import Path

__all__ = ["binary_path", "census_build", "x13_arima_analysis"]


def binary_path() -> Path:
    path = Path(str(files("x13as") / "_bin" / "x13as"))
    if not path.exists():
        raise FileNotFoundError(f"x13as binary not found at {path}")
    if not os.access(path, os.X_OK):
        path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return path


def census_build() -> str:
    return (files("x13as") / "_bin" / "BUILD").read_text().strip()


def x13_arima_analysis(endog, **kwargs):
    """statsmodels.tsa.x13.x13_arima_analysis with the bundled binary."""
    from statsmodels.tsa.x13 import x13_arima_analysis as _x13

    kwargs.setdefault("x12path", str(binary_path()))
    return _x13(endog, **kwargs)


def _cli() -> None:
    binary = str(binary_path())
    os.execv(binary, [binary, *sys.argv[1:]])
