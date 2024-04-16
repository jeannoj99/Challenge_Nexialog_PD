import pandas as pd
from utils.utils import convert_numeric_to_category

# b (binaires)
data_for_binary = pd.read_csv("../data/app_data_binary.csv")
binary_vars_for_app =['FLAG_MOBIL', 'FLAG_EMP_PHONE', 'FLAG_WORK_PHONE', 'FLAG_CONT_MOBILE', 'FLAG_PHONE', 'FLAG_EMAIL', 'REG_REGION_NOT_LIVE_REGION', 'REG_REGION_NOT_WORK_REGION', 'LIVE_REGION_NOT_WORK_REGION', 'REG_CITY_NOT_LIVE_CITY', 'REG_CITY_NOT_WORK_CITY', 'LIVE_CITY_NOT_WORK_CITY']

# lc (faibles modalités)
lc_vars_for_app = ['NAME_CONTRACT_TYPE', 'FLAG_OWN_CAR', 'FLAG_OWN_REALTY', 'FONDKAPREMONT_MODE', 'HOUSETYPE_MODE', 'EMERGENCYSTATE_MODE', 'HAS_CHILDREN', 'REGION_RATING_CLIENT', 'REGION_RATING_CLIENT_W_CITY']
low_category_non_stable_vars=["FLAG_OWN_REALTY", "FONDKAPREMONT_MODE", "HOUSETYPE_MODE", "EMERGENCYSTATE_MODE"]
data_for_lc = pd.read_csv("../data/app_data_lc.csv")

# hc (grd nbr moda)
hc_vars_for_app_nd= ['NAME_EDUCATION_TYPE', 'NAME_FAMILY_STATUS', 'NAME_HOUSING_TYPE', 'NAME_INCOME_TYPE', 'NAME_TYPE_SUITE', 'OCCUPATION_TYPE', 'ORGANIZATION_TYPE', 'WALLSMATERIAL_MODE', 'WEEKDAY_APPR_PROCESS_START']

# liste fausse
hc_vars_for_app_d =['AMT_ANNUITY', 'AMT_CREDIT', 'AMT_CREDIT_NORM', 'AMT_CREDIT_TO_INCOME', 'AMT_GOODS_PRICE', 'AMT_INCOME_TOTAL', 'AMT_INCOME_TOTAL_NORM', 'BORROWER_AGE', 'BORROWER_FIDELITY', 'BORROWER_SENIORITY', 'CB_AMT_ANNUITY', 'CB_AMT_CREDIT_SUM', 'CB_AMT_CREDIT_SUM_DEBT', 'CB_DAYS_CREDIT', 'CB_DAYS_CREDIT_ENDDATE', 'CB_NB_CREDIT_CLOSED', 'DAYS_LAST_PHONE_CHANGE', 'FAM_STATS_CHILD', 'NAME_EDUCATION_TYPE', 'NAME_FAMILY_STATUS_2', 'OCCUPATION_TYPE']

# dataset qui a les variables NON DISCRETISEES NUMERIQUES
data_for_hc_nd = pd.read_csv("../data/app_hc_no_disc.csv")

#dataset qui a les variables discrétisées numériques
data_for_hc_d_train = pd.read_csv("../data/app_hc_disc_train.csv")
# TODO Supprimer (CSV) car non utilisé 
# data_for_hc_d_test = pd.read_csv("../data/app_hc_disc_test.csv")

catego_a_utiliser= ['FLAG_EMP_PHONE', 'OCCUPATION_TYPE', 
                    'WALLSMATERIAL_MODE', 'FLAG_WORK_PHONE',
                      'REGION_RATING_CLIENT', 'ORGANIZATION_TYPE',
                        'FLAG_OWN_CAR', 'FLAG_PHONE', 'HAS_CHILDREN',
                          'NAME_EDUCATION_TYPE', 'NAME_HOUSING_TYPE',
                            'NAME_TYPE_SUITE', 'REG_CITY_NOT_LIVE_CITY',
                              'NAME_CONTRACT_TYPE', 'REGION_RATING_CLIENT_W_CITY', 
                              'NAME_FAMILY_STATUS', 'LIVE_CITY_NOT_WORK_CITY',
                                'REG_CITY_NOT_WORK_CITY', 'NAME_INCOME_TYPE']


# variables numériques qui deviendront discrétisées
discretised_cols=["AMT_INCOME_TOTAL_NORM", "AMT_CREDIT_TO_INCOME" , "BORROWER_AGE", "BORROWER_SENIORITY",
                  "BORROWER_FIDELITY", "AMT_CREDIT_NORM", "DAYS_LAST_PHONE_CHANGE",
                  "AMT_ANNUITY","AMT_GOODS_PRICE", "CB_DAYS_CREDIT",
                  'CB_AMT_CREDIT_SUM_DEBT', 'CB_NB_CREDIT_CLOSED', 
                  'CB_DAYS_CREDIT_ENDDATE', 'CB_AMT_CREDIT_SUM', 'CB_AMT_ANNUITY']

# variables numériques qui ne seront PAS discrétisées !
tested_numerical_variables=[
    "BORROWER_AGE","BORROWER_SENIORITY","BORROWER_FIDELITY","AMT_INCOME_TOTAL_NORM",
    "AMT_CREDIT_NORM", "AMT_INCOME_TOTAL","AMT_CREDIT",
    "AMT_ANNUITY","AMT_GOODS_PRICE",
    'CB_AMT_CREDIT_SUM_DEBT', 'CB_NB_CREDIT_ACTIVE', 'CB_NB_CREDIT_CLOSED', 'CB_DAYS_CREDIT', 'CB_DAYS_CREDIT_ENDDATE', 'CB_AMT_CREDIT_SUM', 'CB_AMT_ANNUITY'
]