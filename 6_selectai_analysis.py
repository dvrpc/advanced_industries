#Author: Brian Carney
#Last updated: 09/10/2021
#Purpose: This script analyzes the select advanced industries profiled in the advanced industries report (NAICS: 3345, 5417, 3345)

#Import packages
import pandas as pd
import numpy as np
from functools import reduce

#Import indexes

#NAICS 4-digit Industry Groups
NAICS_IG = pd.read_csv("G:\\Shared drives\\Community & Economic Development\\Advanced Industries_2021\\naics-crosswalks\\NAICS_2017_4Digit_Index.csv", index_col="NAICS")
NAICS_IG.index = NAICS_IG.index.astype('str')

#Advanced Industries
advanced = pd.read_csv("G:\\Shared drives\\Community & Economic Development\\Advanced Industries_2021\\AdvancedIndustries_Index.csv", dtype={'NAICS':str}, index_col='NAICS')
advanced.index = advanced.index.astype('str')

#Import data

#CBP 2018
cbp18_raw = pd.read_csv("G:\\My Drive\\DataAnalysis\\CBP_2018\\cbp18co.txt", dtype={'fipstate': str, 'fipscty': str, })

#QCEW 2019
qcew19_raw = pd.read_csv("G:\\My Drive\\DataAnalysis\\BLS_QCEW_2019\\2019.annual.singlefile.csv", dtype={'area_fips': str, 'industry_code': str, 'own_code': str, 'agglvl_code': str})

#Select 4-digit NAICS
cbp18_fourdigitnaics = cbp18_raw.loc[(cbp18_raw['naics'].str.contains('//')) & ~(cbp18_raw['naics'].str.contains('///'))]
cbp18_fourdigitnaics['NAICS'] = cbp18_fourdigitnaics['naics'].str.slice(start=0, stop=4)
cbp18_fourdigitnaics['fips'] = cbp18_fourdigitnaics['fipstate'] + cbp18_fourdigitnaics['fipscty']

cbp18_fourdigitnaics = cbp18_fourdigitnaics[['fips','NAICS', 'emp']]
cbp18_fourdigitnaics['US_TotalEmp'] = cbp18_fourdigitnaics['emp'].sum()

#Calculate Total Employment for each Industry Group
cbp18_IGtotalemp_df = cbp18_fourdigitnaics[['NAICS', 'emp']]
cbp18_IG_totalemp = cbp18_IGtotalemp_df.groupby('NAICS').sum()
cbp18_IG_totalemp.rename(columns = {"emp": "IG_TotalEmp"}, inplace=True)

#Join Industry Group Totals in with CBP 2018 df
cbp18_industryjoin = cbp18_fourdigitnaics.merge(cbp18_IG_totalemp, how="left", left_on="NAICS", right_index=True)

#Calculate Total Employment for each county
cbp18_countyEmp_df = cbp18_fourdigitnaics[['fips', 'emp']]
cbp18_countyEmp = cbp18_countyEmp_df.groupby('fips').sum()
cbp18_countyEmp.rename(columns = {'emp': 'county_TotalEmp'}, inplace=True)

#Join County Totals in with CBP 2018 Industry Group DF
cbp18_joined_DFs = cbp18_industryjoin.merge(cbp18_countyEmp, how="left", left_on="fips", right_on="fips")
print(cbp18_joined_DFs)

#Reduce QCEW DF
qcew19 = qcew19_raw.loc[(qcew19_raw['own_code'] == '5') & (qcew19_raw['agglvl_code'] == '76')]
qcew19 = qcew19[['area_fips', 'industry_code', 'annual_avg_wkly_wage']]
qcew19.rename(columns={'industry_code': 'NAICS', 'area_fips': 'fips'}, inplace=True)
print(qcew19)

#Join CBP DF with QCEW DF
cbp18_qcew19 = cbp18_joined_DFs.merge(qcew19, how="left", left_on=["NAICS", "fips"], right_on=["NAICS", "fips"])
print(cbp18_qcew19)

#Select DVRPC region based on fips
dvrpcFIPS = ['34005', '34007', '34015', '34021', '42017', '42029', '42045', '42091', '42101']
dvrpc_18 = cbp18_qcew19.loc[cbp18_qcew19['fips'].isin(dvrpcFIPS)]

print(dvrpc_18)

#Focus Industry Groups
def focusIGs(x):
    d = {}
    d['naics3345_emp'] = x.loc[x['NAICS'] == '3345', 'emp'].sum()
    d['naics3345_avgwklywg'] = x.loc[x['NAICS'] == '3345', 'annual_avg_wkly_wage'].mean()
    d['naics5417_emp'] = x.loc[x['NAICS'] == '5417', 'emp'].sum()
    d['naics5417_avgwklywg'] = x.loc[x['NAICS'] == '5417', 'annual_avg_wkly_wage'].mean()
    d['naics6215_emp'] = x.loc[x['NAICS'] == '6215', 'emp'].sum()
    d['naics6215_avgwklywg'] = x.loc[x['NAICS'] == '6215', 'annual_avg_wkly_wage'].mean()
    d['naics3254_emp'] = x.loc[x['NAICS'] == '3254', 'emp'].sum()
    d['naics3254_avgwklywg'] = x.loc[x['NAICS'] == '3254', 'annual_avg_wkly_wage'].mean()
    d['county_emp'] = x['emp'].sum()
    return pd.Series(d, index=['naics3345_emp', 'naics3345_avgwklywg', 'naics5417_emp', 'naics5417_avgwklywg', 'naics6215_emp', 'naics6215_avgwklywg', 'naics3254_emp', 'naics3254_avgwklywg', 'county_emp'])

countyemp_wklywg_df = dvrpc_18.groupby('fips').apply(focusIGs)
print(countyemp_wklywg_df)


#Calculate industry group employment
naics3345_ig_emp = cbp18_fourdigitnaics.loc[cbp18_fourdigitnaics['NAICS'] == '3345', 'emp'].sum()
naics5417_ig_emp = cbp18_fourdigitnaics.loc[cbp18_fourdigitnaics['NAICS'] == '5417', 'emp'].sum()
naics6215_ig_emp = cbp18_fourdigitnaics.loc[cbp18_fourdigitnaics['NAICS'] == '6215', 'emp'].sum()
naics3254_ig_emp = cbp18_fourdigitnaics.loc[cbp18_fourdigitnaics['NAICS'] == '3254', 'emp'].sum()

dvrpc_18['LQ'] = round((dvrpc_18['emp']/dvrpc_18['county_TotalEmp'])/(dvrpc_18['IG_TotalEmp']/dvrpc_18['US_TotalEmp']), 2)
print(dvrpc_18)

topIndustryGroups = ['3345', '5417', '6215', '3254']

dvrpc_topIGs_18 = dvrpc_18.loc[dvrpc_18['NAICS'].isin(topIndustryGroups)]
dvrpc_topIGs_18.set_index(['fips', 'NAICS'], inplace=True)
print(dvrpc_topIGs_18)

dvrpc_topIGs_18.to_csv("G:\\Shared drives\\Community & Economic Development\\Advanced Industries_2021\\python-exports\\counties-advanced-cbp.csv")
