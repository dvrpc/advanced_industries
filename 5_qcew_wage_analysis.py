#Author: Brian Carney
#Last updated: 08/13/2021
#Prepared for: Advanced Industries report
#Purpose: This script uses QCEW 2010 and 2019 data to calculate the average weekly wage for Advanced Industries and compare them to the average US wage.

import pandas as pd
import numpy as np

#Import QCEW 2010 Data
qcew10_raw = pd.read_csv("G:\\My Drive\\DataAnalysis\\BLS_QCEW_2010\\2010.annual.singlefile.csv", dtype={'area_fips': str, 'own_code': str, 'industry_code': str, 'agglvl_code': str})
print(qcew10_raw)

#Select agglvl_code '10' (National, total covered) to get national average weekly wage
qcew10_national = qcew10_raw.loc[qcew10_raw['agglvl_code'] == '10']
print(qcew10_national)

#Inflation Adjustment: Jan 2010 to Jan 2019 (per https://www.bls.gov/data/inflation_calculator.htm)
inflationAdjustment = 1.16164

#Calculate inflation-adjusted national average weekly wage for QCEW 2010 data
qcew10_national = qcew10_national[['own_code','annual_avg_wkly_wage']]
qcew10_national['annual_avg_wkly_wage_ia'] = round(qcew10_national['annual_avg_wkly_wage'] * inflationAdjustment, 2)
qcew10_national_avgWklyWage_ia = qcew10_national.iloc[0,2]
print("The inflation-adjusted national average weekly wage in 2010 was ${}".format(qcew10_national_avgWklyWage_ia))

#County average weekly wage
qcew10_counties = qcew10_raw.loc[(qcew10_raw['agglvl_code'] == '70') & (qcew10_raw['area_fips'].isin(['34005', '34007', '34015', '34021', '42017', '42029', '42045', '42091', '42101']))]
qcew10_counties = qcew10_counties[['area_fips', 'annual_avg_wkly_wage']]
qcew10_counties['annual_avg_wkly_wage_ia'] = round(qcew10_counties['annual_avg_wkly_wage'] * inflationAdjustment, 2)
print(qcew10_counties)

#County Average Weekly Wages
qcew10_burAvgWklyWage_ia = qcew10_counties.iloc[0,2]
qcew10_camAvgWklyWage_ia = qcew10_counties.iloc[1,2]
qcew10_gloAvgWklyWage_ia = qcew10_counties.iloc[2,2]
qcew10_merAvgWklyWage_ia = qcew10_counties.iloc[3,2]
qcew10_bucAvgWklyWage_ia = qcew10_counties.iloc[4,2]
qcew10_cheAvgWklyWage_ia = qcew10_counties.iloc[5,2]
qcew10_delAvgWklyWage_ia = qcew10_counties.iloc[6,2]
qcew10_monAvgWklyWage_ia = qcew10_counties.iloc[7,2]
qcew10_phiAvgWklyWage_ia = qcew10_counties.iloc[8,2]

print('The 2010 average weekly wage for Burlington County was ${}'.format(qcew10_burAvgWklyWage_ia))
print('The 2010 average weekly wage for Camden County was ${}'.format(qcew10_camAvgWklyWage_ia))
print('The 2010 average weekly wage for Gloucester County was ${}'.format(qcew10_gloAvgWklyWage_ia))
print('The 2010 average weekly wage for Mercer County was ${}'.format(qcew10_merAvgWklyWage_ia))
print('The 2010 average weekly wage for Bucks County was ${}'.format(qcew10_bucAvgWklyWage_ia))
print('The 2010 average weekly wage for Chester County was ${}'.format(qcew10_cheAvgWklyWage_ia))
print('The 2010 average weekly wage for Delaware County was ${}'.format(qcew10_delAvgWklyWage_ia))
print('The 2010 average weekly wage for Montgomery County was ${}'.format(qcew10_monAvgWklyWage_ia))
print('The 2010 average weekly wage for Philadelphia County was ${}'.format(qcew10_phiAvgWklyWage_ia))

#Import QCEW 2019 data
qcew19_raw = pd.read_csv("G:\\My Drive\\DataAnalysis\\BLS_QCEW_2019\\2019.annual.singlefile.csv", dtype={'area_fips': str, 'own_code': str, 'industry_code': str, 'agglvl_code': str})
print(qcew19_raw)

#Select agglvl_code '10' to get national average weekly wage
qcew19_national = qcew19_raw.loc[qcew19_raw['agglvl_code'] == '10']
print(qcew19_national)

qcew19_national = qcew19_national[['own_code','annual_avg_wkly_wage']]
qcew19_national_avgWklyWage = qcew19_national.iloc[0,1]
print('The national average weekly wage in 2019 was ${}'.format(qcew19_national_avgWklyWage))

#Merge QCEW 2010 and 2019 DFs to calculate the change in the average weekly wage from 2010 to 2019
#Select agglvl_code 16 and private sector (own_code = 5) to select National data at 4-digit NAICS level
qcew10_agglvl_16 = qcew10_raw.loc[(qcew10_raw['agglvl_code'] == '16') & (qcew10_raw['own_code'] == '5')]
qcew10_agglvl_16= qcew10_agglvl_16[['industry_code', 'annual_avg_emplvl', 'annual_avg_wkly_wage']]
print(qcew10_agglvl_16)

#Add inflation adjusted column (Inflation multiplier: 1.16164)
qcew10_agglvl_16['avgwklywg10_ia'] = round(qcew10_agglvl_16['annual_avg_wkly_wage'] * 1.16164, 0)
qcew10_agglvl_16.rename(columns={'annual_avg_emplvl': '2010: Average Employment', 'annual_avg_wkly_wage': '2010: Average Weekly Wage (Raw)', 'avgwklywg10_ia': '2010: Average Weekly Wage (Inflation-adjusted)'},inplace=True)
print(qcew10_agglvl_16)

#QCEW 2019
qcew19_agglvl_16 = qcew19_raw.loc[(qcew19_raw['agglvl_code'] == '16') & (qcew19_raw['own_code'] == '5')]
qcew19_agglvl_16 = qcew19_agglvl_16[['industry_code', 'annual_avg_emplvl', 'annual_avg_wkly_wage']]
qcew19_agglvl_16.rename(columns={'annual_avg_emplvl': '2019: Average Employment', 'annual_avg_wkly_wage': '2019: Average Weekly Wage'},inplace=True)
print(qcew19_agglvl_16)

#Merge QCEW 2010 and QCEW 2019 DFs
qcew_join_industrygroups = qcew10_agglvl_16.merge(qcew19_agglvl_16, how="inner", on="industry_code")
qcew_join_industrygroups['Wages: Percent Change'] = round(100 * (qcew_join_industrygroups['2019: Average Weekly Wage'] - qcew_join_industrygroups['2010: Average Weekly Wage (Inflation-adjusted)'])/(qcew_join_industrygroups['2010: Average Weekly Wage (Inflation-adjusted)']), 1)
qcew_join_industrygroups['Employment: Percent Change'] = round(100 * (qcew_join_industrygroups['2019: Average Employment'] - qcew_join_industrygroups['2010: Average Employment'])/(qcew_join_industrygroups['2010: Average Employment']), 1)
qcew_join_industrygroups.rename(columns={'industry_code': 'NAICS'}, inplace=True)
print(qcew_join_industrygroups)

#Import Advanced Industries Index
advanced = pd.read_csv("G:\\Shared drives\\Community & Economic Development\\Advanced Industries_2021\\AdvancedIndustries_Index.csv", dtype={'NAICS': str})
print(advanced)

#Join Merged QCEW DF to Advanced Industries index
qcew_advanced_join = advanced.merge(qcew_join_industrygroups, how="left", on="NAICS")
qcew_advanced_join.set_index('NAICS', inplace=True)
print(qcew_advanced_join)

#Calculations:
#Total employment for advanced industries
#adv_empweight = Each industry's total employment divided by overall employment
#avg_wageweight = Employment Weight multiplied by the average weekly wage
#adv_avgwklywage = Sum of Wage Weights for each Industry Group. Weighted Average Weekly Wage for Advanced Industries.
adv_totalemp_19 = qcew_advanced_join['2019: Average Employment'].sum()
adv_empweight = qcew_advanced_join['2019: Average Employment']/adv_totalemp_19
qcew_advanced_join['adv_wageweight'] = round(adv_empweight * qcew_advanced_join['2019: Average Weekly Wage'], 3)
adv_avgwklywage = round(qcew_advanced_join['adv_wageweight'].sum(), 2)

print("The weighted average weekly wage for advanced industries is ${}.".format(adv_avgwklywage))

#Advanced Industries
#Average Employment Change from 2010 to 2019
adv_aggemp_10 = qcew_advanced_join['2010: Average Employment'].sum()
adv_aggemp_19 = qcew_advanced_join['2019: Average Employment'].sum()
advanced_empchange = round(100 * (adv_aggemp_19 - adv_aggemp_10)/(adv_aggemp_10), 1)
print("Total employment in advanced industries increased by {} percent from 2010 to 2019.".format(advanced_empchange))

#Non-advanced Industries
#Average Employment Change from 2010 to 2019
qcew_nonadvanced = qcew_join_industrygroups[~qcew_join_industrygroups['NAICS'].isin(advanced['NAICS'])]
na_aggemp_10 = qcew_nonadvanced['2010: Average Employment'].sum()
na_aggemp_19 = qcew_nonadvanced['2019: Average Employment'].sum()
nonadvanced_empchange = round(100 * (na_aggemp_19 - na_aggemp_10)/(na_aggemp_10), 1)
print("Total employment in non-advanced industries increased by {} percent from 2010 to 2019.".format(nonadvanced_empchange))

#Aggregated Average Weekly Wage for Non-advanced Industries
na_totalemp_19 = qcew_nonadvanced['2019: Average Employment'].sum()
na_empweight = qcew_nonadvanced['2019: Average Employment']/na_totalemp_19
qcew_nonadvanced['na_wageweight'] = round(na_empweight * qcew_nonadvanced['2019: Average Weekly Wage'], 3)
na_avgwklywage = round(qcew_nonadvanced['na_wageweight'].sum(), 2)
print("The weighted average weekly wage for non-advanced industries is ${}.".format(na_avgwklywage))

print("The average weekly wage for advanced industries is ${}, which is {} percent higher than the average weekly wage of non-advanced industries at ${}.".format(adv_avgwklywage, round((adv_avgwklywage-na_avgwklywage)/na_avgwklywage*100,1),na_avgwklywage))