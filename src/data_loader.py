"""
data_loader.py
"""

import pandas as pd


def load_giwaxs(path):

    df = pd.read_csv(
        path,
        comment="#",
        sep=r"\s+",
        header=None
    )

    if df.shape[1] >= 3:

        df = df.iloc[:, :3]

        df.columns = [
            "Q",
            "Intensity",
            "Error"
        ]

    else:

        df = df.iloc[:, :2]

        df.columns = [
            "Q",
            "Intensity"
        ]

        df["Error"] = 1.0

    return df