from pathlib import Path

import pandas as pd

from azure_batch_testing import average_iris_column

pd.DataFrame = average_iris_column("sepal.width").to_csv(Path(__file__).parent.parent / "output" / "sepal_width.csv")
print("Sepal width done")