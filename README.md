# Advanced Industries

This project analyzes advanced industries in the nine-county Delaware Valley Regional Planning Commission (DVRPC) region.
The term "advanced industries" comes from a 2015 Brookings report, "America's Advanced Industries: What They Are, Where They Are, and Why They Matter." To qualify as an advanced industry, an industry group (4-digit NAICS code) must meet the following criteria:

- “R&D spending exceeds $450 per worker, as measured by the National Science Foundation’s 2009 Business R&D and Innovation Survey (BRDIS), which equates to roughly the 80th percentile of spending intensity”
- “Over 21 percent--above the U.S. average--of an industry’s workforce can be found in occupations requiring a high degree of STEM knowledge as defined by O*NET”

## Data
This project primarily uses two data sources: County Business Patterns (CBP) and the Bureau of Labor Statistics (BLS) Quarterly Census of Employment & Wages (QCEW). CBP data is primarily used for employment, while QCEW data is used for wage analysis. The following zip files were saved locally as csv's.

### CBP

#### County-level
2010: https://www2.census.gov/programs-surveys/cbp/datasets/2010/cbp10co.zip

2018: https://www2.census.gov/programs-surveys/cbp/datasets/2018/cbp18co.zip?#

#### National-level
2010: https://www2.census.gov/programs-surveys/cbp/datasets/2010/cbp10us.zip

2018: https://www2.census.gov/programs-surveys/cbp/datasets/2018/cbp18us.zip?#

### QCEW

#### Single File
2019: https://data.bls.gov/cew/data/files/2019/csv/2019_annual_singlefile.zip

## Scripts

### 1_clean_cbp.py
This script cleans and joins 2018 County Business Patterns (CBP) industry employment data. It breaks the data down at the county, region, and national level.

### 2_clean_qcew.py
This script uses BLS QCEW 2019 data to calculate the average weekly wages for advanced industries in the DVRPC region.

### 3_cbp_empchg.py
This script takes CBP 2010 and 2018 data at the national and looks at the change in employment in the US overall and in the Advanced Industries Industry Groups.

### 4_cbp_qcew_join.py
This script joins cleaned CBP (from script 1) and QCEW (from script 2) data for Advanced Industries and exports it to an Excel Workbook.

### 5_qcew_wage_analysis.py
This script uses QCEW 2010 and 2019 data to calculate the average weekly wage for Advanced Industries and compare them to the average US wage.

The average weekly wage is weighted based on total county employment. Each county's employment was divided by the region's total employment to get its employment share. The employment share was then multiplied by the average weekly wage to get the weighted wage share. The sum of the weighted wage shares yields the weighted average weekly wage.

### 6_selectai_analysis.py
This script analyzes the select advanced industries profiled in the advanced industries report (NAICS: 3345, 5417, 3345).

### 7_consolidate_export.py
This script joins cleaned CBP (from script no. 1) and QCEW (from script no. 2) data for Advanced Industries and exports it to an Excel Workbook.
