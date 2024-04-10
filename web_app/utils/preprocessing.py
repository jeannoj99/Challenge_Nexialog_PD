import pandas as pd
from utils.utils import convert_numeric_to_category

data=pd.read_csv("../data/application_train_vf.csv",parse_dates=["date_mensuelle"], index_col=0)

# importation de données d'autre base préparées
credit_bureau_data=pd.read_csv("../data/cb_findings.csv", index_col=0)
data=data.merge(credit_bureau_data, left_on="SK_ID_CURR", right_on="CB_SK_ID_CURR")

# feature engineering
data["HAS_CHILDREN"]=data["CNT_CHILDREN"].apply(lambda x : "Y" if x > 0 else "N")
data.drop(columns=["CNT_CHILDREN"], inplace=True)

drop_documents_cols= [f"FLAG_DOCUMENT_{i}" for i in range(2, 22)]

data.drop(columns=drop_documents_cols, inplace=True)
convert_numeric_to_category(data)
data["date_annee"]=data["date_mensuelle"].dt.year #annee
out_of_sample_data=data[data["date_annee"]==2020] # echantillon out-of-sample
data=data[data["date_annee"]<2020] # echantillon in-sample

#save for app
data_for_binary = data.copy(deep=True)

categorical_vars=data.select_dtypes(include="object").columns.tolist()
numerical_vars=data.select_dtypes(include="number").columns.tolist()
binary_vars=[var for var in numerical_vars if (data[var].nunique()==2)&(var !="TARGET")]

#save for app
binary_vars_for_app = [{'label':var,'value':var} for var in binary_vars]

binary_risk_non_stable_vars=["FLAG_MOBIL", "FLAG_CONT_MOBILE", "FLAG_EMAIL", "REG_REGION_NOT_LIVE_REGION", "REG_REGION_NOT_WORK_REGION","LIVE_REGION_NOT_WORK_REGION"]
binary_vars=list(filter(lambda x : x not in binary_risk_non_stable_vars, binary_vars))

binary_volume_non_stable_vars=[]
binary_non_stable_vars=list(set(binary_volume_non_stable_vars+binary_risk_non_stable_vars))
binary_vars=list(filter(lambda x : x not in binary_non_stable_vars,binary_vars))

data.drop(columns=binary_non_stable_vars, inplace=True)
numerical_vars=list(filter(lambda x : x not in binary_vars+binary_non_stable_vars,numerical_vars))
low_category_categorical_vars=[var for var in categorical_vars+numerical_vars if  (var not in binary_vars+binary_non_stable_vars+["TARGET"]) & (data[var].nunique()>=2) & (data[var].nunique()<=4)]

# save for app
lc_vars_for_app =  [{'label':var,'value':var} for var in low_category_categorical_vars]

low_category_non_stable_vars=["FLAG_OWN_REALTY", "FONDKAPREMONT_MODE", "HOUSETYPE_MODE", "EMERGENCYSTATE_MODE", "CODE_GENDER"]

updated_low_category_categorical_vars=list(filter(lambda x : x not in low_category_non_stable_vars,low_category_categorical_vars))

#save for app
data_for_lc = data.copy(deep=True)

data.drop(columns=low_category_non_stable_vars)

categorical_vars=list(filter(lambda x : x not in binary_non_stable_vars+binary_vars+updated_low_category_categorical_vars+low_category_non_stable_vars, categorical_vars))



