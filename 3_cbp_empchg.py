#Author: Brian Carney
#Purpose: This script takes CBP 2010 and 2018 data at the national and looks at the change in employment in the US overall and in the Advanced Industries Industry Groups.
#Last updated: 08/26/2021

#Import packages
import pandas as pd
import numpy as np

#Import 2010 CBP national data
cbp10_raw = pd.read_csv("G:\\My Drive\\DataAnalysis\\CBP_2010\\NationalLevel\\cbp10us.txt")

#Select 4-digit NAICS and lfo '-' (all establishments)
cbp10_IG = cbp10_raw.loc[cbp10_raw['naics'].str.contains('//') & ~ cbp10_raw['naics'].str.contains('///') & (cbp10_raw['lfo'] == '-')]
cbp10_IG['naics_four'] = cbp10_IG['naics'].str.slice(start=0, stop = 4)
cbp10_IG = cbp10_IG[['naics_four', 'emp']]
cbp10_IG.rename(columns = {'emp': 'emp10'}, inplace=True)
cbp10_IG.set_index('naics_four', inplace=True)

#Import 2018 CBP national data
cbp18_raw = pd.read_csv("G:\\My Drive\\DataAnalysis\\CBP_2018\\NationalLevel\\cbp18us.txt")

#Select 4-digit NAICS and lfo '-' (all establishments)
cbp18_IG = cbp18_raw.loc[cbp18_raw['naics'].str.contains('//') & ~ cbp18_raw['naics'].str.contains('///') & (cbp18_raw['lfo'] == '-')]
cbp18_IG['naics_four'] = cbp18_IG['naics'].str.slice(start=0, stop = 4)
cbp18_IG = cbp18_IG[['naics_four', 'emp']]
cbp18_IG.rename(columns = {'emp': 'emp18'}, inplace=True)
cbp18_IG.set_index('naics_four', inplace=True)

#Crosswalk for NAICS changes from 2012 to 2017
cbp10_IG.rename(index = {'4523': '4529'}, inplace=True)
cbp10_IG.rename(index = {'5173': '5171'}, inplace=True)
cbp10_IG.rename(index = {'5173': '5172'}, inplace=True)

#Join DFs
cbp_join = cbp10_IG.merge(cbp18_IG, how="outer", left_index=True, right_index=True)
cbp_join.index = cbp_join.index.rename('NAICS')

#Import Advanced Industries Index
advanced = pd.read_csv("G:\\Shared drives\\Community & Economic Development\\Advanced Industries_2021\\AdvancedIndustries_Index.csv", dtype={'NAICS': str})
advanced['advanced'] = '1'

#Join Advanced Industries Index with joined CBP DF
cbp_advanced_join = advanced.merge(cbp_join, how="left", left_on='NAICS', right_index=True)
cbp_advanced_join.set_index(['NAICS', 'Industry Title', 'Category'], inplace=True)

#Create column that measures the percent change in industry group employment from 2010 to 2018
cbp_advanced_join['Change'] = round(100 * (cbp_advanced_join['emp18'] - cbp_advanced_join['emp10'])/cbp_advanced_join['emp10'], 1)

advanced_reduced = advanced[['NAICS', 'advanced']]
advanced_reduced.set_index('NAICS', inplace=True)

#Create DF with Advanced and Non-Advanced Industries for comparison
cbp_allIGs = cbp_join.merge(advanced_reduced, how="left", left_index=True, right_index= True)

#Calculate Total Employment Change for Advanced Industries
advanced_df = cbp_allIGs.loc[cbp_allIGs['advanced'] == '1']
advanced_TotalEmpChg = (advanced_df['emp18'].sum()) - (advanced_df['emp10'].sum())
advanced_pctTotalEmpChg = round(100 * (advanced_TotalEmpChg/(advanced_df['emp10'].sum())), 2)
print(advanced_pctTotalEmpChg)

#Calculate Total Employment Change for Non-Advanced Industries
nonAdvanced_df = cbp_allIGs.loc[cbp_allIGs['advanced'] != '1']
nonAdvanced_TotalEmpChg = (nonAdvanced_df['emp18'].sum()) - (nonAdvanced_df['emp10'].sum())
nonAdvanced_pctTotalEmpChg = round(100 * (nonAdvanced_TotalEmpChg/(nonAdvanced_df['emp10'].sum())), 2)
print(nonAdvanced_pctTotalEmpChg)

print("From 2010 to 2018, total employment in non-advanced industries in the U.S. grew by {} percent, while total employment in advanced industries grew by {} percent.".format(nonAdvanced_pctTotalEmpChg, advanced_pctTotalEmpChg))

#Export to csv
cbp_advanced_join.to_csv("G:\\Shared drives\\Community & Economic Development\\Advanced Industries_2021\\python-exports\\national-advanced-cbp.csv")


cbp_allIGs['emp_chg'] = round(100 * (cbp_allIGs['emp18']-cbp_allIGs['emp10'])/cbp_allIGs['emp10'], 1)
print(cbp_allIGs)

median_empChg_allIGs = cbp_allIGs['emp_chg'].median()
print(median_empChg_allIGs)

print(nonAdvanced_pctTotalEmpChg)