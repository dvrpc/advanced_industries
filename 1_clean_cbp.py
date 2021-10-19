#Author: Brian Carney
#Purpose: This script cleans and joins 2018 County Business Patterns (CBP) industry employment data. It breaks the data down at the county, region, and national level.
#Last Updated: 08/18/2021

#Import packages
import pandas as pd 
import numpy as np
from functools import reduce

#Import NAICS Industry Group Index
NAICS_IG = pd.read_csv("G:\\Shared drives\\Community & Economic Development\\Advanced Industries_2021\\naics-crosswalks\\NAICS_4Digit_Index.csv", index_col="NAICS")
NAICS_IG.index = NAICS_IG.index.astype('str')

#Import Advanced Industries Index
advanced = pd.read_csv("G:\\Shared drives\\Community & Economic Development\\Advanced Industries_2021\\AdvancedIndustries_Index.csv", dtype={'NAICS':str}, index_col='NAICS')
advanced.index = advanced.index.astype('str')

#Import 2018 CBP Data
cbp18_raw = pd.read_csv("G:\\My Drive\\DataAnalysis\\CBP_2018\\cbp18co.txt", dtype={'fipstate': str, 'fipscty': str})

#Select 4-digit NAICS from 2018 CBP
cbp18_fourdigitnaics = cbp18_raw.loc[(cbp18_raw['naics'].str.contains('//')) & ~(cbp18_raw['naics'].str.contains('///'))]
cbp18_fourdigitnaics['naics_four'] = cbp18_fourdigitnaics['naics'].str.slice(start=0, stop=4)
cbp18_fourdigitnaics['fips'] = cbp18_fourdigitnaics['fipstate'] + cbp18_fourdigitnaics['fipscty']

#Condense 2018 CBP DF and calculate total U.S. employment
cbp18_condensed = cbp18_fourdigitnaics[['fips','naics_four', 'emp']]
cbp18_condensed['US_TotalEmp'] = cbp18_condensed['emp'].sum()

#Calculate total employment for each industry group
cbp18_IGtotalemp_df = cbp18_condensed[['naics_four', 'emp']]
cbp18_IG_totalemp = cbp18_IGtotalemp_df.groupby('naics_four').sum()
cbp18_IG_totalemp.rename(columns = {"emp": "IG_TotalEmp"}, inplace=True)

#Join industry group totals in with 2018 CBP DF
cbp18_industryjoin = cbp18_condensed.merge(cbp18_IG_totalemp, how="left", left_on="naics_four", right_index=True)
print(cbp18_industryjoin)

#Select DVRPC region based on FIPS
dvrpc_18 = cbp18_industryjoin.loc[cbp18_industryjoin['fips'].isin(['34005', '34007', '34015', '34021', '42017', '42029', '42045', '42091', '42101'])]

#Calculate total employment in region
dvrpc_18['Region_TotalEmp'] = dvrpc_18['emp'].sum()

#Condense DF to calculate industry group employment within region
dvrpc_ig_18 = dvrpc_18[['naics_four', 'emp']]
dvrpc_ig_totals = dvrpc_ig_18.groupby('naics_four').sum()
dvrpc_ig_totals.rename(columns={"emp": "Region_IG_TotalEmp"}, inplace=True)

#Join region industry group total employment DF back in with 2018 CBP DF
dvrpc_18_igjoined = dvrpc_18.merge(dvrpc_ig_totals, how="left", left_on="naics_four", right_index=True)

#Drop duplicates
dvrpc_18_duplicatedf = dvrpc_18_igjoined[['naics_four', 'US_TotalEmp', 'IG_TotalEmp', 'Region_TotalEmp', 'Region_IG_TotalEmp']]
dvrpc_18_nodupes = dvrpc_18_duplicatedf.drop_duplicates()

#Join Advanced Industries Index with DF
dvrpc18_cbp_advanced = advanced.merge(dvrpc_18_nodupes, how="left", left_index=True, right_on='naics_four')

#Calculate LQ for industry groups in region
dvrpc18_cbp_advanced['LQ'] = round((dvrpc18_cbp_advanced['Region_IG_TotalEmp']/dvrpc18_cbp_advanced['Region_TotalEmp'])/(dvrpc18_cbp_advanced['IG_TotalEmp']/dvrpc18_cbp_advanced['US_TotalEmp']), 2)
dvrpc18_cbp_advanced.rename(columns={'naics_four': 'NAICS'}, inplace=True)
dvrpc18_cbp_advanced.set_index('NAICS', inplace=True)

#Export to csv
dvrpc18_cbp_advanced.to_csv("G:\\Shared drives\\Community & Economic Development\\Advanced Industries_2021\\python-exports\\region-advanced-cbp.csv")