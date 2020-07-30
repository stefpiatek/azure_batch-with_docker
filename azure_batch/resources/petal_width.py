from pathlib import Path

import pandas as pd

from azure_batch_testing import average_iris_column

output_dir = Path(__file__).parent / "output"
output_dir.mkdir(exist_ok=True)
pd.DataFrame = average_iris_column("petal.width").to_csv(output_dir / "petal_width.csv")
print("Petal width done")