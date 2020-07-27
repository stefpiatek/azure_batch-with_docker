"""Main module."""
from pathlib import Path

import pandas as pd


def average_iris_column(column):
    return pd.read_csv(Path(__file__).parent.parent / "resources" /"iris.csv").groupby("variety").sum().loc[:, [column]]


if __name__ == "__main__":
    print(average_iris_column("petal.width"))
