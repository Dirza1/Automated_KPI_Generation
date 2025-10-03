from pathlib import Path
from classes import product,customer,region
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
   #In the example file with one excell sheet we used a dictionaty with a list. For this one we are gonne make it a bit more complicated. 
   #We are gonna make a class system for the indivigual products and clients. Look in the classes.py file for the classes.

   north:region = region()
   south:region = region()
   east:region = region()
   west:region = region()

   widgeta:product = product()
   widgetb:product = product()
   widgetc:product = product()

   gammainc:customer = customer()
   betaltd:customer = customer()
   acmecorp:customer = customer()

   #now we have instansiates the classes we need for this KPI generation.
   #obiusly this is very restricive when adding new customers or products but when you are eitehr small
   #or high in a large company and work with summaries this is an option.

   for file in files_in_current_path:
        filepath:str = "./report_excels/" + file
        datafile:DataFrame = pd.read_excel(filepath)
        
        gamme = datafile[(datafile["Customer"] == "Gamma Inc")]
        betal = datafile[(datafile["Customer"] == "Beta Ltd")]
        acme = datafile[(datafile["Customer"] == "Acne Corp")]

        nor =  datafile[(datafile["Region"] == "North")]
        eas = datafile[(datafile["Region"] == "East")]
        wes = datafile[(datafile["Region"] == "West")]
        sout = datafile[(datafile["Region"] == "South")]

        a = datafile[(datafile["Product"] == "Widget A")]
        b = datafile[(datafile["Product"] == "Widget B")]
        c= datafile[(datafile["Product"] == "Widget C")]

        print(c)
      
if __name__ == "__main__":
    main()
