from pathlib import Path
from collections import defaultdict
import os
import pandas as pd 
from pandas import DataFrame,Series # type: ignore


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
            #The way we do this makes it a bit les flexible, but there are ways around this aswel. For example aan json file with products so we caan filter on all products.
            #For this show case I will not implement them, but it is possible
           total_customer_data[month][row[1][2]]["Quantity"] += row[1][5]
           total_customer_data[month][row[1][2]]["Total Value"] += row[1][5] * row[1][6]
           total_customer_data[month][row[1][2]][row[1][3]] += row[1][5]
           total_customer_data[month][row[1][2]][row[1][4]] += row[1][5]

if __name__ == "__main__":
    main()
