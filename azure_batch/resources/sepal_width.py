from pathlib import Path

import pandas as pd

from azure_batch_testing import average_iris_column

output_dir = Path(__file__).parent / "output"
output_dir.mkdir(exist_ok=True)
pd.DataFrame = average_iris_column("sepal.width").to_csv(output_dir / "sepal_width.csv")
print("Sepal width done")