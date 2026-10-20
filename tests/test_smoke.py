import pandas as pd
from statsmodels.datasets import macrodata

import x13as


def test_binary_is_executable():
    assert x13as.binary_path().stat().st_mode & 0o111


def test_x11_adjustment_runs():
    df = macrodata.load_pandas().data
    index = pd.period_range("1959Q1", periods=len(df), freq="Q").to_timestamp()
    y = pd.Series(df["realcons"].to_numpy(), index=index)
    res = x13as.x13_arima_analysis(y, outlier=True, trading=False, log=True)
    assert len(res.seasadj) == len(y)
    assert res.seasadj.notna().all()
    assert "X-13ARIMA-SEATS" in res.results
