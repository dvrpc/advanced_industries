#Author: Brian Carney
#Purpose: This script joins cleaned CBP (from script 1) and QCEW (from script 2) data for Advanced Industries and exports it to an Excel Workbook
#Last Updated: 08/19/2021

#Import packages
import pandas as pd 
import numpy as np
from functools import reduce

#Insert CBP DF
cbp_advanced = pd.read_csv("G:\\Shared drives\\Community & Economic Development\\Advanced Industries_2021\\python-exports\\dvrpc18_cbp_advanced.csv", dtype={'naics_four': str})
cbp_advanced.rename(columns={'naics_four': 'NAICS'}, inplace = True)
cbp_advanced.set_index(['NAICS'], inplace=True)

#Insert QCEW DF
qcew_advanced = pd.read_csv("G:\\Shared drives\\Community & Economic Development\\Advanced Industries_2021\\python-exports\\qcew_advanced_clean_join.csv", dtype={'naics_four': str})
qcew_advanced.rename(columns={'naics_four': 'NAICS'}, inplace = True)
qcew_advanced.set_index(['NAICS'], inplace=True)

#Join CBP DF with QCEW DF
merged_dfs = cbp_advanced.merge(qcew_advanced, how="left", left_index=True, right_index=True)
nonull_merged_dfs = merged_dfs.loc[merged_dfs['Region_TotalEmp'].notnull()]
nonull_merged_dfs = nonull_merged_dfs[['Region_IG_TotalEmp', 'LQ', 'weighted_avg_wkly_wage', 'nat_avg_wkly_wage', 'reg_wg_diff']]
nonull_merged_dfs.rename(columns= {'Region_IG_TotalEmp': 'Employment - Regional', 'weighted_avg_wkly_wage': 'Average Weekly Wage - Region', 'nat_avg_wkly_wage': 'Average Weekly Wage - National', 'reg_wg_diff': 'Difference'}, inplace=True)

#Import Advanced Industries Index
advanced = pd.read_csv("G:\\Shared drives\\Community & Economic Development\\Advanced Industries_2021\\AdvancedIndustries_Index.csv", dtype={'NAICS': str})
advanced.set_index('NAICS', inplace=True)
advanced = advanced[['Industry Title', 'Category']]

#Join Advanced Industries Index with merged DF
advanced_mergedDFs_join = advanced.merge(nonull_merged_dfs, how="left", left_index=True, right_index=True)

#Export to csv
advanced_mergedDFs_join.to_csv("G:\\Shared drives\\Community & Economic Development\\Advanced Industries_2021\\python-exports\\region-advanced-cbp-qcew.csv")