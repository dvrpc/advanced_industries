#Author: Brian Carney
#Last Updated: 08/18/2021
#Purpose: This script joins cleaned CBP (from script no. 1) and QCEW (from script no. 2) data for Advanced Industries and exports it to an Excel Workbook

#Import packages
import pandas as pd 
import numpy as np
from functools import reduce

#Import DFs
df1 = pd.read_csv("G:\\Shared drives\\Community & Economic Development\\Advanced Industries_2021\\python-exports\\region-advanced-cbp.csv", index_col='NAICS')
df2 = pd.read_csv("G:\\Shared drives\\Community & Economic Development\\Advanced Industries_2021\\python-exports\\region-advanced-qcew.csv", index_col='NAICS')
df3 = pd.read_csv("G:\\Shared drives\\Community & Economic Development\\Advanced Industries_2021\\python-exports\\national-advanced-cbp.csv", index_col='NAICS')
df4 = pd.read_csv("G:\\Shared drives\\Community & Economic Development\\Advanced Industries_2021\\python-exports\\region-advanced-cbp-qcew.csv", index_col='NAICS')
df5 = pd.read_csv("G:\\Shared drives\\Community & Economic Development\\Advanced Industries_2021\\python-exports\\counties-advanced-cbp.csv", index_col = 'fips')

with pd.ExcelWriter("G:\\Shared drives\\Community & Economic Development\\Advanced Industries_2021\\python-exports\\combined-dfs.xlsx") as writer:
    df1.to_excel(writer, sheet_name='region-cbp')
    df2.to_excel(writer, sheet_name='region-qcew')
    df3.to_excel(writer, sheet_name='nation-cbp')
    df4.to_excel(writer, sheet_name='region-cbp-qcew')
    df5.to_excel(writer, sheet_name='counties-cbp')
