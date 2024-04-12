import pandas as pd
from utils.utils import convert_numeric_to_category

# b (binaires)
data_for_binary = pd.read_csv("../data/app_data_binary.csv")
binary_vars_for_app = [{'label': 'FLAG_MOBIL', 'value': 'FLAG_MOBIL'}, {'label': 'FLAG_EMP_PHONE', 'value': 'FLAG_EMP_PHONE'}, {'label': 'FLAG_WORK_PHONE', 'value': 'FLAG_WORK_PHONE'}, {'label': 'FLAG_CONT_MOBILE', 'value': 'FLAG_CONT_MOBILE'}, {'label': 'FLAG_PHONE', 'value': 'FLAG_PHONE'}, {'label': 'FLAG_EMAIL', 'value': 'FLAG_EMAIL'}, {'label': 'REG_REGION_NOT_LIVE_REGION', 'value': 'REG_REGION_NOT_LIVE_REGION'}, {'label': 'REG_REGION_NOT_WORK_REGION', 'value': 'REG_REGION_NOT_WORK_REGION'}, {'label': 'LIVE_REGION_NOT_WORK_REGION', 'value': 'LIVE_REGION_NOT_WORK_REGION'}, {'label': 'REG_CITY_NOT_LIVE_CITY', 'value': 'REG_CITY_NOT_LIVE_CITY'}, {'label': 'REG_CITY_NOT_WORK_CITY', 'value': 'REG_CITY_NOT_WORK_CITY'}, {'label': 'LIVE_CITY_NOT_WORK_CITY', 'value': 'LIVE_CITY_NOT_WORK_CITY'}]

# lc (faibles modalités)
lc_vars_for_app =  [{'label': 'NAME_CONTRACT_TYPE', 'value': 'NAME_CONTRACT_TYPE'}, {'label': 'CODE_GENDER', 'value': 'CODE_GENDER'}, {'label': 'FLAG_OWN_CAR', 'value': 'FLAG_OWN_CAR'}, {'label': 'FLAG_OWN_REALTY', 'value': 'FLAG_OWN_REALTY'}, {'label': 'FONDKAPREMONT_MODE', 'value': 'FONDKAPREMONT_MODE'}, {'label': 'HOUSETYPE_MODE', 'value': 'HOUSETYPE_MODE'}, {'label': 'EMERGENCYSTATE_MODE', 'value': 'EMERGENCYSTATE_MODE'}, {'label': 'HAS_CHILDREN', 'value': 'HAS_CHILDREN'}, {'label': 'REGION_RATING_CLIENT', 'value': 'REGION_RATING_CLIENT'}, {'label': 'REGION_RATING_CLIENT_W_CITY', 'value': 'REGION_RATING_CLIENT_W_CITY'}]
low_category_non_stable_vars=["FLAG_OWN_REALTY", "FONDKAPREMONT_MODE", "HOUSETYPE_MODE", "EMERGENCYSTATE_MODE", "CODE_GENDER"]
data_for_lc = pd.read_csv("../data/app_data_lc.csv")

# hc (grd nbr moda)
hc_vars_for_app_nd= ['NAME_EDUCATION_TYPE', 'NAME_FAMILY_STATUS', 'NAME_HOUSING_TYPE', 'NAME_INCOME_TYPE', 'NAME_TYPE_SUITE', 'OCCUPATION_TYPE', 'ORGANIZATION_TYPE', 'WALLSMATERIAL_MODE', 'WEEKDAY_APPR_PROCESS_START']
hc_vars_for_app_d =['AMT_ANNUITY', 'AMT_CREDIT', 'AMT_CREDIT_NORM', 'AMT_CREDIT_TO_INCOME', 'AMT_GOODS_PRICE', 'AMT_INCOME_TOTAL', 'AMT_INCOME_TOTAL_NORM', 'BORROWER_AGE', 'BORROWER_FIDELITY', 'BORROWER_SENIORITY', 'CB_AMT_ANNUITY', 'CB_AMT_CREDIT_SUM', 'CB_AMT_CREDIT_SUM_DEBT', 'CB_DAYS_CREDIT', 'CB_DAYS_CREDIT_ENDDATE', 'CB_NB_CREDIT_CLOSED', 'DAYS_LAST_PHONE_CHANGE', 'FAM_STATS_CHILD', 'NAME_EDUCATION_TYPE', 'NAME_FAMILY_STATUS_2', 'OCCUPATION_TYPE']
data_for_hc_nd = pd.read_csv("../data/app_hc_no_disc.csv")
data_for_hc_d_train = pd.read_csv("../data/app_hc_disc_train.csv")
data_for_hc_d_test = pd.read_csv("../data/app_hc_disc_test.csv")
