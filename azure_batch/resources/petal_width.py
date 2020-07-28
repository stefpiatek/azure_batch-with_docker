from pathlib import Path

import pandas as pd

from azure_batch_testing import average_iris_column

pd.DataFrame = average_iris_column("petal.width").to_csv(Path(__file__).parent.parent / "output" / "petal_width.csv")
print("Petal width done")