"""Run the actual copy-and-paste example against the installed wheel."""

import re
from pathlib import Path

import numpy as np
import pandas as pd


def test_readme_example(capsys):
    readme = (Path(__file__).resolve().parents[1] / "README.md").read_text()
    examples = re.findall(r"```python\n(.*?)```", readme, flags=re.DOTALL)
    assert len(examples) == 1, "Keep this test aligned with the documented examples"
    namespace = {}
    exec(compile(examples[0], "README.md", "exec"), namespace)

    sales = namespace["sales"]
    result = namespace["result"]
    assert len(sales) == 60
    for series in (result.seasadj, result.trend):
        pd.testing.assert_index_equal(series.index, sales.index)
        assert np.isfinite(series.to_numpy()).all()
    assert not np.allclose(result.seasadj, sales)
    assert "adjusted" in capsys.readouterr().out
