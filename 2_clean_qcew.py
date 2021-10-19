#Author: Brian Carney
#Purpose: This script uses BLS QCEW 2019 data to calculate the average weekly wages for advanced industries in the DVRPC region
#Last updated: 08/19/2021

#Import packages
import pandas as pd
import numpy as np

#Import industry groups index
NAICS_IG = pd.read_csv("G:\\Shared drives\\Community & Economic Development\\Advanced Industries_2021\\naics-crosswalks\\NAICS_4Digit_Index.csv", dtype= {'NAICS': str}, index_col="NAICS")

#Import Advanced Industries index
advanced = pd.read_csv("G:\\Shared drives\\Community & Economic Development\\Advanced Industries_2021\\AdvancedIndustries_Index.csv", dtype={'NAICS':str}, index_col='NAICS')
advanced.index = advanced.index.astype('str')

#Import BLS QCEW 2019 data
qcew19_raw = pd.read_csv("G:\\My Drive\\DataAnalysis\\BLS_QCEW_2019\\2019.annual.singlefile.csv", dtype={'area_fips': str, 'industry_code': str})

#Select agglvl_code 16 (national, 4-digit NAICS) and own_code 5 (private) to get avg wkly wage at the national level
national_4digit = qcew19_raw.loc[(qcew19_raw['agglvl_code'] == 16) & (qcew19_raw['own_code'] == 5)]
national_4digit = national_4digit[['industry_code','annual_avg_wkly_wage']]
national_4digit.rename(columns={'annual_avg_wkly_wage': 'nat_avg_wkly_wage'}, inplace=True)

#Select agglvl_code 76 (county, 4-digit NAICS) and own_code 5 (private)
qcew19_agglvl_76_owncode_5 = qcew19_raw.loc[(qcew19_raw['agglvl_code'] == 76) & (qcew19_raw['own_code'] == 5)]

#Select DVRPC region based on FIPS
qcew19_dvrpc = qcew19_agglvl_76_owncode_5.loc[qcew19_agglvl_76_owncode_5['area_fips'].isin(['34005', '34007', '34015', '34021', '42017', '42029', '42045', '42091', '42101'])]
qcew19_dvrpc = qcew19_dvrpc[['area_fips', 'industry_code', 'annual_avg_emplvl', 'annual_avg_wkly_wage']]

#Calculate total employment for each industry group
qcew19_IG_owncode_total = qcew19_dvrpc[['industry_code', 'annual_avg_emplvl']]
IG_OwnCode_Totals = qcew19_IG_owncode_total.groupby(['industry_code']).sum()
IG_OwnCode_Totals.rename(columns= {'annual_avg_emplvl': 'Industry_TotalEmp'}, inplace=True)
IG_OwnCode_Totals

#Join industry group total employment DF back in with DVRPC region DF
qcew_IGOwnCode_join = qcew19_dvrpc.merge(IG_OwnCode_Totals, how="inner", left_on=["industry_code"], right_on=["industry_code"])

#Calculate wage weight
qcew_IGOwnCode_join['wage_weight'] = qcew_IGOwnCode_join['annual_avg_emplvl']/qcew_IGOwnCode_join['Industry_TotalEmp']
qcew_IGOwnCode_join['avg_wkly_wg_wt'] = qcew_IGOwnCode_join['annual_avg_wkly_wage'] * qcew_IGOwnCode_join['wage_weight']

#Group by industry_code to get the weighted wages for the region's industry groups
qcew_condensed_wage_wt = qcew_IGOwnCode_join[['industry_code', 'avg_wkly_wg_wt']]
qcew_weightedwg = round(qcew_condensed_wage_wt.groupby(['industry_code']).sum(), 2)
qcew_weightedwg.rename(columns={'avg_wkly_wg_wt': 'weighted_avg_wkly_wage'}, inplace=True)

#Join Advanced Industries Index with region weighted wage DF
qcew_advanced = advanced.merge(qcew_weightedwg, how="left", left_index=True, right_on="industry_code")

#Join national, private 4-digit NAICS DF with region, private 4-digit NAICS DF
qcew_advanced_join = qcew_advanced.merge(national_4digit, how="left", left_on="industry_code", right_on = "industry_code")
qcew_advanced_join['reg_wg_diff'] = round(((qcew_advanced_join['weighted_avg_wkly_wage'] - qcew_advanced_join['nat_avg_wkly_wage'])/qcew_advanced_join['nat_avg_wkly_wage']) * 100, 2)
qcew_advanced_join.rename(columns={'industry_code': 'NAICS', 'category': 'Category'}, inplace=True)
qcew_advanced_join.set_index(['NAICS', 'Industry Title','Category'], inplace=True)

#Export to csv
qcew_advanced_join.to_csv("G:\\Shared drives\\Community & Economic Development\\Advanced Industries_2021\\python-exports\\region-advanced-qcew.csv")