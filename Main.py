from pathlib import Path
from collections import defaultdict
import os
import pandas as pd 
from pandas import DataFrame


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
    KPI_names:list = ["Quantity","Total Value","North","East","South","West", "Widget A", "Widget B", "Widget C"]
    #TODO, report writing in diferent method return a DF. Pass the list needed. 2 extra lists with customers and product and those are inputs in the writer method
    rows_customers:list = []    
    for month in months:
        if month in total_customer_data:
            for customer in customer_names:
                if customer in total_customer_data[month]:
                    for KPI in KPI_names:
                        if KPI in total_customer_data[month][customer]:
                            rows_customers.append({"Month":month, "Customer": customer, "KPI": KPI, "Value": total_customer_data[month][customer][KPI]})
    
    df_long = pd.DataFrame(rows_customers)

    df_pivot = df_long.pivot(index="KPI",columns=['Month','Customer'],values='Value')

    df_pivot = df_pivot.fillna(0).replace("", 0)

    df_pivot = df_pivot.reindex(KPI_names)

    df_pivot = df_pivot.reindex(columns=pd.MultiIndex.from_product([months, customer_names], names=['Month', 'Customer']))

    df_pivot.columns.names = ["Month","Customer"]

    df_pivot.to_excel("test.xlsx")
        
    
if __name__ == "__main__":
    main()
