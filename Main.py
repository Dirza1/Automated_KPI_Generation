from pathlib import Path
from collections import defaultdict
import os
import pandas as pd 
from pandas import DataFrame
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

def main()->None:
    """
    This function will make a new KPI dashbord from multiple diferent reports. For this example we will suimmarise monthly sales reports
    """
    #first we will find the subfolder with the reports and we wil get a list of all the files that are there.
    #we can if needed sort here for only .xlsx for example. For this example we dont need to as we know there are only excel reports.
    #we can also ensure there are only report that contain sales in the name for example.
    current_path:str = os.getcwd() 
    files_in_current_path:list = os.listdir(current_path + "/report_excels")
    filepaths:list = []
    for file in files_in_current_path:
       filepaths.append(current_path + "/" + file)
    

   #after getting the files we will define the data structures we need to contain the information.
   #Same as with the other script we will use a dictionary. This dictionary will have a bit more of a complex structure.
   #as we dont only want the data we also want the assosiated month with it. So the keys in the dictionary will be the month wich will hold multiple other dictionarys.

    total_customer_data:defaultdict = defaultdict(
        lambda: defaultdict(
            lambda: defaultdict(int)
        )
    )
    total_product_data:defaultdict = defaultdict(
        lambda: defaultdict(
            lambda: defaultdict(int)
        )
    )
    total_region_data:defaultdict = defaultdict(
        lambda: defaultdict(
            lambda: defaultdict(int)
        )
    )

    #so we haave one dictionary for each KPI we aare interested in.
    #now we can populate them

    for file in files_in_current_path:
        filepath:str = "./report_excels/" + file
        datafile:DataFrame = pd.read_excel(filepath)
         
         #so now we are in our file we need to transform the name of the file to the month. So we need to strip the "sales_" prefix and xlsx postfix
        month:str = file.removeprefix("sales_").removesuffix(".xlsx")
        
        #we are now reaady to start filling the data

        for row in datafile.iterrows():
            #we first take all the KPI's needed for the customers. Quantity, Totl value, Total per regon, Total per product
            #Due to this we are verry flexible with customers and products. If you add one its no issue
            total_customer_data[month][row[1][2]]["Quantity"] += row[1][5]
            total_customer_data[month][row[1][2]]["Total Value"] += row[1][5] * row[1][6]
            total_customer_data[month][row[1][2]][row[1][3]] += row[1][5]
            total_customer_data[month][row[1][2]][row[1][4]] += row[1][5]

            total_product_data[month][row[1][4]]["Quantity"] += row[1][5]
            total_product_data[month][row[1][4]]["Total Value"] += row[1][5] * row[1][6]
            total_product_data[month][row[1][4]][row[1][2]] += row[1][5] 
            total_product_data[month][row[1][4]][row[1][3]] += row[1][5]

            total_region_data[month][row[1][3]]["Quantity"] += row[1][5]
            total_region_data[month][row[1][3]]["Total Value"] += row[1][5] * row[1][6]
            total_region_data[month][row[1][3]][row[1][2]] += row[1][5] 
            total_region_data[month][row[1][3]][row[1][4]] += row[1][5]

        #We now have all the date from all the files ordered by month (or name of the file).
        #We can now start building the KPI. We will make a new file with all the data sorted. That way we can use this file aswel and have all the sorted data.
        #we will make 3 tabs in this new excel one for KIP per product, one for customers and one for regions
        #hoever to ensure that we are consistent in our excell we need to define some values first. I hard code them here but we cna make then dinamic

    months:list = ["jan", "feb", "mar","apr"] #extend for the full year
    customer_names:list = ["Gamma Inc","Beta Ltd","Acme Corp"] #all customer names
    product_naames:list = ["Widget A", "Widget B", "Widget C"]
    region_names:list = ["North", "East","South","West"]
    KPI_names:list = ["Quantity","Total Value","North","East","South","West", "Widget A", "Widget B", "Widget C","Gamma Inc","Beta Ltd","Acme Corp"]
        
    customer_df:DataFrame = generate_dataframe(data = total_customer_data,months=months,columns=customer_names,KPIs=KPI_names)
    product_df:DataFrame = generate_dataframe(data = total_product_data,columns=product_naames,KPIs= KPI_names,months=months)
    region_df:DataFrame = generate_dataframe(data=total_region_data,months=months,columns=region_names,KPIs=KPI_names)

    #write the data to an excell sheet.    
    with pd.ExcelWriter("Sales KPI's.xlsx") as writer:
        customer_df.to_excel(writer, sheet_name="Customers")
        product_df.to_excel(writer,"Products")
        region_df.to_excel(writer,"regions")

    #now to make some nice pictures
    make_dashboard(customer_df,product_df,region_df)

def make_dashboard(customer_df, product_df, region_df, outdir="figures"):
    """
    Generate KPI charts from the customer, product, and region DataFrames
    and save them as PNG files.
    """

    # Ensure the output directory exists
    os.makedirs(outdir, exist_ok=True)

    # === Customer KPIs ===
    # Quantity per customer
    quantity_df = customer_df.loc["Quantity"]
    quantity_df.plot(kind="bar")
    plt.title("Quantity per customer per month")
    plt.ylabel("Units")
    plt.savefig(f"{outdir}/quantity_per_customer.png", bbox_inches="tight")
    plt.close()

    # Total Value per customer
    total_value_df = customer_df.loc["Total Value"]
    total_value_df.T.plot(marker="o")
    plt.title("Total Value per customer per month")
    plt.ylabel("Value (€)")
    plt.savefig(f"{outdir}/total_value_per_customer.png", bbox_inches="tight")
    plt.close()

    # Regional distribution stacked bar
    regions = ["North", "East", "South", "West"]
    region_split = customer_df.loc[regions]
    region_split.T.plot(kind="bar", stacked=True)
    plt.title("Regional distribution per customer/month")
    plt.ylabel("Units")
    plt.savefig(f"{outdir}/region_distribution.png", bbox_inches="tight")
    plt.close()

    # Product mix stacked bar
    widgets = ["Widget A", "Widget B", "Widget C"]
    product_split = customer_df.loc[widgets]
    product_split.T.plot(kind="bar", stacked=True)
    plt.title("Product mix per customer/month")
    plt.ylabel("Units")
    plt.savefig(f"{outdir}/product_mix.png", bbox_inches="tight")
    plt.close()

    # === Product KPIs ===
    prod_quantity_df = product_df.loc["Quantity"]
    prod_quantity_df.plot(kind="bar")
    plt.title("Quantity per product per month")
    plt.ylabel("Units")
    plt.savefig(f"{outdir}/quantity_per_product.png", bbox_inches="tight")
    plt.close()

    # === Region KPIs ===
    reg_quantity_df = region_df.loc["Quantity"]
    reg_quantity_df.plot(kind="bar")
    plt.title("Quantity per region per month")
    plt.ylabel("Units")
    plt.savefig(f"{outdir}/quantity_per_region.png", bbox_inches="tight")
    plt.close()

def generate_dataframe(data:defaultdict, months:list, columns:list,KPIs:list) -> DataFrame:
    """
    This function creates a DataFrame for the excel file.
    It takes the data, the 3 layerd dictionary, The months we want as main columns, the cub colums aand the KPI's.
    It then renerates a DataFrame to be written to a xlsx file
    """
    #remove the column names from the KPI's
    subKPI:list = KPIs.copy()
    for value in columns:
        if value in subKPI:
            subKPI.remove(value)
    
    #Generate a list with the dictionaries to write to excel 
    rows_customers:list = []    
    for month in months:
        if month in data:
            for column in columns:
                if column in data[month]:
                    for KPI in subKPI:
                        if KPI in data[month][column]:
                            rows_customers.append({"Month":month, "Column": column, "KPI": KPI, "Value": data[month][column][KPI]})
    
    df_long = pd.DataFrame(rows_customers)

    #create  picot and reindex on KPI's
    df_pivot = df_long.pivot(index="KPI",columns=['Month','Column'],values='Value')

    df_pivot = df_pivot.fillna(0).replace("", 0)

    df_pivot = df_pivot.reindex(subKPI)

    df_pivot = df_pivot.reindex(columns=pd.MultiIndex.from_product([months, columns], names=['Month', 'Column']))

    df_pivot.columns.names = ["Month","Column"]

    return df_pivot
    
    
if __name__ == "__main__":
    main()


