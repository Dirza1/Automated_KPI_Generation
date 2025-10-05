# Automated KPI Dashboard Generator

📌 **Project Description**  
This project demonstrates an automated way to generate KPI dashboards from monthly sales reports using Python. It is designed for leadership teams to quickly visualize sales performance without manual Excel work. The script aggregates multiple months of sales data, generates Excel summaries, and produces presentation-ready charts.

The script:

- Reads multiple monthly Excel reports from a folder.
- Creates three Excel sheets: KPIs per Product, Customer, and Region.
- Generates PNG charts for easy presentation inclusion.

---

## ⚙️ Features

✅ Automatically aggregates sales data across multiple months.  
✅ Generates KPI summaries per Customer, Product, and Region.  
✅ Produces PNG charts for Quantity, Total Value, Product Mix, and Regional Distribution.  
✅ Saves all results in an Excel file and a folder of charts.

---

## 🛠️ Requirements

- **Python 3.12+**  
- Libraries:
  - pandas
  - matplotlib

Install dependencies:

```bash
pip install pandas matplotlib
```

---

## ▶️ Usage

1. Place your monthly Excel report files in the `report_excels` folder next to the script.  
   - File names should follow the pattern `sales_<month>.xlsx` (e.g., `sales_jan.xlsx`).  
2. Run the script:

```bash
python main.py
```

3. Outputs:
   - `Sales KPI's.xlsx` containing three sheets:
     - Customers
     - Products
     - Regions
   - `figures/` folder containing PNG charts for presentation use.

---

## 📊 Example Output

**Customer KPI Summary (Excel)**

| Customer   | Quantity | Total Value | North | East | South | West |
|------------|----------|-------------|-------|-----|-------|------|
| Gamma Inc  | 81       | 2740        | 31    | 7   | 24    | 19   |
| Beta Ltd   | 85       | 1780        | 32    | 46  | 7     | 0    |
| Acme Corp  | 73       | 1995        | 21    | 36  | 0     | 16   |

**Generated charts (PNG):**

- `quantity_per_customer.png`  
- `total_value_per_customer.png`  
- `region_distribution.png`  
- `product_mix.png`  
- `quantity_per_product.png`  
- `quantity_per_region.png`  

---

## 📂 Project Structure

```
.
├── main.py                 # Main script
├── report_excels/          # Folder with monthly sales Excel files
├── Sales KPI's.xlsx        # Output Excel file with aggregated KPI data
├── figures/                # Generated charts as PNG files
└── README.md               # Project documentation
```

---

## 📖 Portfolio Highlight

This project showcases:

- Automating Excel-based KPI dashboards with Python.  
- Practical use of pandas for data aggregation and pivoting.  
- Automated chart generation with matplotlib for presentation-ready visuals.  
- Handling multiple months of sales data in a structured, reusable workflow.

---

## 💡 Future Enhancements

- Generate interactive dashboards (e.g., with Plotly or Dash).  
- Embed charts directly into the Excel sheets.  
- Add more KPI metrics or filtering options for advanced analytics.
