import pandas as pd # type: ignore
from pathlib import Path
import numpy as np # type: ignore

# Output folder
output_dir = Path("report_excels")
output_dir.mkdir(parents=True, exist_ok=True)

# Customers, products, regions for fake data
customers = ["Acme Corp", "Beta Ltd", "Gamma Inc", "Delta BV"]
products = ["Widget A", "Widget B", "Widget C"]
regions = ["North", "East", "West", "South"]

def create_sample_excel(filename: Path, start_order_id: int, start_date: str, end_date: str, n_rows: int = 20):
    """
    Create one Excel file with sample sales data.
    
    Args:
        filename (Path): File path to save Excel file.
        start_order_id (int): Starting OrderID for this file.
        start_date (str): Start date for random order dates.
        end_date (str): End date for random order dates.
        n_rows (int): Number of rows to generate.
    """
    dates = pd.date_range(start=start_date, end=end_date, freq="3D")
    data = {
        "OrderID": [start_order_id + i for i in range(n_rows)],
        "Date": np.random.choice(dates, size=n_rows),
        "Customer": np.random.choice(customers, size=n_rows),
        "Region": np.random.choice(regions, size=n_rows),
        "Product": np.random.choice(products, size=n_rows),
        "Quantity": np.random.randint(5, 25, size=n_rows),
        "UnitPrice": np.random.choice([15.0, 25.0, 40.0], size=n_rows)
    }
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"Generated {filename}")

if __name__ == "__main__":
    # Generate 4 monthly Excel files
    create_sample_excel(output_dir/"sales_jan.xlsx", 1001, "2024-01-01", "2024-01-31")
    create_sample_excel(output_dir/"sales_feb.xlsx", 2001, "2024-02-01", "2024-02-29")
    create_sample_excel(output_dir/"sales_mar.xlsx", 3001, "2024-03-01", "2024-03-31")
    create_sample_excel(output_dir/"sales_apr.xlsx", 4001, "2024-04-01", "2024-04-30")
    
    print("✅ All 4 sample Excel files generated in 'project2_excels/' folder.")
