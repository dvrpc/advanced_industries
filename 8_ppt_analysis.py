#Author: Brian Carney
#Last updated: 09/28/2021
#Purpose: This script provides data needed for the Advanced Industries ppt. 

import pandas as pd
import numpy as np

#Import 2019 QCEW data
qcewRaw = pd.read_csv("G:\\My Drive\\DataAnalysis\\BLS_QCEW_2019\\2019.annual.singlefile.csv", dtype={'area_fips': str, 'own_code': str, 'agglvl_code': str, 'industry_code': str})
print(qcewRaw)

#Select county level aggregation (agglvl_code=76) for all industries (industry_code=10) for DVRPC Counties
qcewDVRPC_long = qcewRaw.loc[(qcewRaw['agglvl_code'] == '76') & (qcewRaw['area_fips'].isin(['34005', '34007', '34015', '34021', '42017', '42029', '42045', '42091', '42101']))]
print(qcewDVRPC_long)

qcewDVRPC = qcewDVRPC_long[['annual_avg_emplvl', 'annual_avg_wkly_wage']]
print(qcewDVRPC)

region_totalEmp = qcewDVRPC['annual_avg_emplvl'].sum()

qcewDVRPC['county_weight'] = (qcewDVRPC['annual_avg_emplvl']/region_totalEmp)
print(qcewDVRPC)

qcewDVRPC['wage_weight'] = qcewDVRPC['annual_avg_wkly_wage'] * qcewDVRPC['county_weight']
dvrpc_avg_wkly_wage = round(qcewDVRPC['wage_weight'].sum(), 2)

print("The weighted average weekly wage for the DVRPC 9-county region is ${}".format(dvrpc_avg_wkly_wage))

#This was calculated as follows:
#1. Sum the total employment in each county to get the total employment for the region
#2. Divide the total employment in each county by the region's total employment (county weight)
#3. Multiply each county's weight by their respective average weekly wage (wage weight)
#4. Sum the wage weight to get the weight average weekly wage for the region

print(region_totalEmp)

#The total employment for the region (per QCEW 2019 data) is 2,733,504 employees

#Import Advanced Industries DF
advanced = pd.read_csv("G:\\Shared drives\\Community & Economic Development\\Advanced Industries_2021\\qcew_advanced_clean_join.csv")
print(advanced['weighted_avg_wkly_wage'])

#Check which industry groups have wage data
advanced_wageData = advanced.loc[advanced['weighted_avg_wkly_wage'].notnull()]

print("Of the 50 advanced industries, {} of them have enough data for our analysis.".format(len(advanced_wageData)))

advanced_higherWage = advanced.loc[advanced['weighted_avg_wkly_wage'] >= dvrpc_avg_wkly_wage]
len(advanced_higherWage)

print("Of the 50 advanced industries, {} of them have a higher average weekly wage than the region's weighted average weekly wage.".format(len(advanced_higherWage)))

#Import Advanced Industries Index
aiIndex = pd.read_csv("G:\\Shared drives\\Community & Economic Development\\Advanced Industries_2021\\AdvancedIndustries_Index.csv", dtype={'NAICS': str})
aiIndex['advanced'] = '1'

#Import CBP 2018 Data
cbp18_raw = pd.read_csv("G:\\My Drive\DataAnalysis\\CBP_2018\\cbp18co.txt", dtype={'fipstate': str, 'fipscty': str, 'naics': str})

#Select 4-digit NAICS from raw CBP 2018 dataframe
cbp18_fourDigit = cbp18_raw.loc[~(cbp18_raw['naics'].str.contains('///')) & (cbp18_raw['naics'].str.contains('//')) & (cbp18_raw['naics'].notnull())]

#Create 4-digit NAICS column for 4-digit NAICS CBP df
cbp18_fourDigit['naics_four'] = cbp18_fourDigit['naics'].str.slice(0,4)

#Create Combined FIPS column
cbp18_fourDigit['fips'] = cbp18_fourDigit['fipstate'] + cbp18_fourDigit['fipscty']

#Join Advanced Industries Index with CBP 2018 data
nationalAdvanced_join = cbp18_fourDigit.merge(aiIndex, how="left", left_on='naics_four', right_on='NAICS')
national_advanced = nationalAdvanced_join.loc[nationalAdvanced_join['advanced'] == '1']
national_nonAdvanced = nationalAdvanced_join.loc[nationalAdvanced_join['advanced'] != '1']
national_nonAdvanced_totalEmp = national_nonAdvanced['emp'].sum()
national_advanced_totalEmp = national_advanced['emp'].sum()
national_totalEmp = cbp18_fourDigit['emp'].sum()

national_pctAdvanced = round(100 * national_advanced_totalEmp/national_totalEmp, 3)

print("Advanced industries account for {} percent of all employment in the U.S., per CBP 2018".format(national_pctAdvanced))

#Select Region based on FIPS
cbp18_region = cbp18_fourDigit.loc[(cbp18_fourDigit['fips'].isin(['34005', '34007', '34015', '34021', '42017', '42029', '42045', '42091', '42101']))]

region_cbpTotalEmp = cbp18_region['emp'].sum()

print("Per 2018 CBP data, the total employment in the region is {}.".format(region_cbpTotalEmp))

cbp18_region_advancedJoin = cbp18_region.merge(aiIndex, how='left', left_on='naics_four', right_on='NAICS')

region_nonAdvanced = cbp18_region_advancedJoin.loc[cbp18_region_advancedJoin['advanced'] != '1']

region_nonAdvanced_totalEmp = region_nonAdvanced['emp'].sum()

print("The total employment for non-advanced industries in the region is {}".format(region_nonAdvanced_totalEmp))

region_advanced = cbp18_region_advancedJoin.loc[cbp18_region_advancedJoin['advanced'] == '1']

region_advanced_totalEmp = region_advanced['emp'].sum()

print("The total employment for advanced industries in the region is {}.".format(region_advanced_totalEmp))

region_pctAdvanced_totalEmp = (round(100 * region_advanced_totalEmp/region_cbpTotalEmp, 2))

print("In the region, advanced industries account for {} percent of total employment, per CBP 2018.".format(region_pctAdvanced_totalEmp))

#Advanced vs non-advanced Wage Comparison

#Select Region from QCEW data
qcew_region_4digit = qcewRaw.loc[(qcewRaw['agglvl_code'] == '76') & (qcewRaw['own_code'] == '5') & (qcewRaw['area_fips'].isin(['34005', '34007', '34015', '34021', '42017', '42029', '42045', '42091', '42101']))]

#Join QCEW data with Advanced Index
region_qcew = qcew_region_4digit.merge(aiIndex, how='left', left_on='industry_code', right_on='NAICS')
list(region_qcew)
region_qcew = region_qcew[['advanced', 'area_fips', 'industry_code', 'annual_avg_emplvl', 'annual_avg_wkly_wage']]

#Calculate weighted average weekly wage for non-advanced industries
region_nonAdvanced_qcew = region_qcew.loc[region_qcew['advanced'].isnull()]
region_nonAdvanced_qcew['weight'] = region_nonAdvanced_qcew['annual_avg_emplvl']/region_nonAdvanced_totalEmp
region_nonAdvanced_qcew['wage_weight'] = region_nonAdvanced_qcew['weight'] * region_nonAdvanced_qcew['annual_avg_wkly_wage']
region_nonAdvanced_avgWklyWg = round(region_nonAdvanced_qcew['wage_weight'].sum(), 2)
print(region_nonAdvanced_avgWklyWg)


#Advanced Industries Category Share
region_advanced_cbp = pd.read_csv("G:\\Shared drives\\Community & Economic Development\\Advanced Industries_2021\\python-exports\\region-advanced-cbp.csv")
advanced_totalEmp = region_advanced_cbp['IG_TotalEmp'].sum()
print(advanced_totalEmp)

cbp_categoryShare_df = region_advanced_cbp[['Category', 'IG_TotalEmp', 'Region_IG_TotalEmp']]
cbp_categoryShare = cbp_categoryShare_df.groupby('Category').sum()

print(national_advanced_totalEmp)
print(region_advanced_totalEmp)

cbp_categoryShare['national_catShare'] = 100 * round(cbp_categoryShare['IG_TotalEmp']/national_advanced_totalEmp, 3)
cbp_categoryShare['region_catShare'] = 100 * round(cbp_categoryShare['Region_IG_TotalEmp']/region_advanced_totalEmp, 3)
print(cbp_categoryShare)

print(cbp_categoryShare['IG_TotalEmp'].sum())
print(national_advanced_totalEmp)

print(region_advanced_cbp.loc[region_advanced_cbp['Category'].notnull(), 'Region_IG_TotalEmp'].sum())

print(national_advanced)
list(national_advanced)

list(cbp18_raw)

cbp18_condensed = cbp18_fourDigit[['naics_four', 'emp']]
cbp18_advanced_join = cbp18_condensed.merge(aiIndex, how="left", left_on='naics_four', right_on='NAICS')
print(cbp18_advanced_join)

usAdvanced_totalEmp = cbp18_advanced_join.loc[cbp18_advanced_join['advanced'] == '1', 'emp'].sum()
print(usAdvanced_totalEmp)

cbp18_categoryshare_df = cbp18_advanced_join[['Category', 'emp']]
cbp18_categoryshare = cbp18_categoryshare_df.groupby('Category').sum()

print(cbp18_categoryshare)

cbp18_categoryshare['nat_catShare'] = 100 * round(cbp18_categoryshare['emp']/usAdvanced_totalEmp, 3)
print(cbp18_categoryshare)