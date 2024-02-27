# import packages 
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from scipy.stats import mannwhitneyu ,chi2_contingency, anderson, f_oneway
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
import statsmodels.api as sm
import warnings
warnings.filterwarnings("ignore")


from src.preprocessing import convert_numeric_to_category, DecisionTreeDiscretizer
from src.tests import cramers_v, mannwhitney_test, calculate_information_value_from_contingency_table, show_conditionnal_density, show_risk_stability_overtime, show_volume_stability_overtime
print("Importation de packages terminée")

data=pd.read_csv("data/application_train_vf.csv",parse_dates=["date_mensuelle"], index_col=0)
data["SK_ID_CURR"].value_counts().max()

# importation de données d'autre base préparées
credit_bureau_data=pd.read_csv("data/cb_findings.csv", index_col=0)
data=data.merge(credit_bureau_data, left_on="SK_ID_CURR", right_on="CB_SK_ID_CURR")

# feature engineering
data["HAS_CHILDREN"]=data["CNT_CHILDREN"].apply(lambda x : "Y" if x > 0 else "N")
data.drop(columns=["CNT_CHILDREN"], inplace=True)

drop_documents_cols=["FLAG_DOCUMENT_2","FLAG_DOCUMENT_3","FLAG_DOCUMENT_4" , 
"FLAG_DOCUMENT_5" , "FLAG_DOCUMENT_6","FLAG_DOCUMENT_7" ,              
"FLAG_DOCUMENT_8" , "FLAG_DOCUMENT_9","FLAG_DOCUMENT_10"  ,"FLAG_DOCUMENT_11" , "FLAG_DOCUMENT_12",              
"FLAG_DOCUMENT_13" ,"FLAG_DOCUMENT_14" ,"FLAG_DOCUMENT_15", "FLAG_DOCUMENT_16" ,
"FLAG_DOCUMENT_17", "FLAG_DOCUMENT_18","FLAG_DOCUMENT_19", "FLAG_DOCUMENT_20","FLAG_DOCUMENT_21"]

data.drop(columns=drop_documents_cols, inplace=True)


convert_numeric_to_category(data)

data["date_annee"]=data["date_mensuelle"].dt.year #annee

out_of_sample_data=data[data["date_annee"]==2020] # echantillon out-of-sample
data=data[data["date_annee"]<2020] # echantillon in-sample

print("Répartition du défaut sur l'échantillon out-sample")
print(out_of_sample_data["TARGET"].value_counts(normalize=True)) # affichage de la répartition du défaut sur l'out-sample
print(40*"=")
print("Répartition du défaut sur l'échantillon in-sample")
print(data["TARGET"].value_counts(normalize=True)) # affichage de la répartition du défaut sur l'in-sample
print(40*"=")


categorical_vars=data.select_dtypes(include="object").columns.tolist()
numerical_vars=data.select_dtypes(include="number").columns.tolist()
binary_vars=[var for var in numerical_vars if (data[var].nunique()==2)&(var !="TARGET")]

print("Stabilité en risque des variables binaires")
for var in binary_vars:
    show_risk_stability_overtime(data,var)


binary_risk_non_stable_vars=["FLAG_MOBIL", "FLAG_CONT_MOBILE", "FLAG_EMAIL", "REG_REGION_NOT_LIVE_REGION", "REG_REGION_NOT_WORK_REGION","LIVE_REGION_NOT_WORK_REGION"]
print(f"Variables binaires non stables : {binary_risk_non_stable_vars}")

binary_vars=list(filter(lambda x : x not in binary_risk_non_stable_vars, binary_vars))

print("Stabilité en volume des variables binaires")
for var in binary_vars:
    show_volume_stability_overtime(data,var)
    
    
binary_volume_non_stable_vars=[]

# variables à virer parmi les binaires:
binary_non_stable_vars=list(set(binary_volume_non_stable_vars+binary_risk_non_stable_vars))

binary_vars=list(filter(lambda x : x not in binary_non_stable_vars,binary_vars))

data.drop(columns=binary_non_stable_vars, inplace=True)

numerical_vars=list(filter(lambda x : x not in binary_vars+binary_non_stable_vars,numerical_vars))

low_category_categorical_vars=[var for var in categorical_vars+numerical_vars if  (var not in binary_vars+binary_non_stable_vars+["TARGET"]) & (data[var].nunique()>=2) & (data[var].nunique()<=4)]

print("Stabilité en volume des variables catégorielles à faible nombre de modalités")
for colname in low_category_categorical_vars:
    show_volume_stability_overtime(data,colname)
    
print("Stabilité en risque des variables catégorielles à faible nombre de modalités")
for col in low_category_categorical_vars:
    show_risk_stability_overtime(data,col)
    
    
low_category_non_stable_vars=["FLAG_OWN_REALTY", "FONDKAPREMONT_MODE", "HOUSETYPE_MODE", "EMERGENCYSTATE_MODE", "CODE_GENDER"]
low_category_categorical_vars=list(filter(lambda x : x not in low_category_non_stable_vars,low_category_categorical_vars))

data.drop(columns=low_category_non_stable_vars)

categorical_vars=list(filter(lambda x : x not in binary_non_stable_vars+binary_vars+low_category_categorical_vars+low_category_non_stable_vars, categorical_vars))

print("Test de chi-2 des autres variables catégorielles et la cible")
for col in categorical_vars:
    n=data.shape[0]
    contingency_table=pd.crosstab(data["TARGET"], data[col])
    chi2, p, _, _ = chi2_contingency(contingency_table, correction=True) #Application d'une correction de Yates par rapport à la faible représentation des classes
    k, r = contingency_table.shape
    v_cramer = np.sqrt(chi2 / (n * min(k-1, r-1)))
    print(f"\nCrosstab for {col}:\n")
    print(contingency_table)
    print("\n" + "-"*40)
    print(f"\nChi-squared: {chi2}")
    print(f"P-value: {p}")
    print(f"Cramer's V: {v_cramer}")
    print("\n" + "="*80)
    
    
print("Stabilité en volume des autres variables catégorielles")   
for col in categorical_vars:
    show_volume_stability_overtime(data,col)
    
data["OCCUPATION_TYPE"].fillna("Unknown", inplace=True)

# groupement proposé pour occupation_type suivant tdf
group_occupation_type={
    0: ['Accountants', 'HR staff', 'High skill tech staff'],
 1: ['Managers', 'Core staff', 'Private service staff', 'Unknown',
        'Medicine staff', 'IT staff', 'Secretaries'],
 2: ['Realty agents', 'Cleaning staff', 'Sales staff', 'Laborers',
        'Cooking staff', 'Security staff'],
 3: ['Drivers', 'Waiters/barmen staff', 'Low-skill Laborers'],
}

data["OCCUPATION_TYPE"]=data["OCCUPATION_TYPE"].map({value: key for key, values in group_occupation_type.items() for value in values})

show_risk_stability_overtime(data,"OCCUPATION_TYPE")
show_volume_stability_overtime(data,"OCCUPATION_TYPE")

# groupement proposé pour education_type suivant tdf
group_education_type={
    "Graduated" : ["Academic degree", "Higher education"],
    "Non graduated":["Lower secondary", "Secondary / secondary special", "Incomplete higher"]
}

data["NAME_EDUCATION_TYPE"]=data["NAME_EDUCATION_TYPE"].map({value: key for key, values in group_education_type.items() for value in values})

show_risk_stability_overtime(data,"NAME_EDUCATION_TYPE")
show_volume_stability_overtime(data,"NAME_EDUCATION_TYPE")

# groupement proposé pour faimily_status suivant tdf
group_family_status={
    "Already_Married": ["Civil marriage", "Married","Separated", "Widow"],
    "Single" :["Single / not married", "Unknown"]
}

data["NAME_FAMILY_STATUS_2"]=data["NAME_FAMILY_STATUS"].map({value: key for key, values in group_family_status.items() for value in values})

show_risk_stability_overtime(data,"NAME_FAMILY_STATUS_2" )
show_volume_stability_overtime(data,"NAME_FAMILY_STATUS_2")

data["FAM_STATS_CHILD"]=data["NAME_FAMILY_STATUS_2"]+"-"+"HAS_CHILDREN_"+data["HAS_CHILDREN"] 

data["FAM_STATS_CHILD"]=data["FAM_STATS_CHILD"].apply(lambda x : "Single" if x in ["Single-HAS_CHILDREN_N","Single-HAS_CHILDREN_Y"] else x)

show_risk_stability_overtime(data, "FAM_STATS_CHILD")
show_volume_stability_overtime(data, "FAM_STATS_CHILD")


social_vars=["OBS_30_CNT_SOCIAL_CIRCLE",
"DEF_30_CNT_SOCIAL_CIRCLE",
"OBS_60_CNT_SOCIAL_CIRCLE",
"DEF_60_CNT_SOCIAL_CIRCLE", "DAYS_LAST_PHONE_CHANGE"
]


for col in social_vars:
    print(mannwhitney_test(data,col, "TARGET"))
    
data["DAYS_LAST_PHONE_CHANGE"].fillna(data["DAYS_LAST_PHONE_CHANGE"].min(), inplace=True)

data["AMT_CREDIT_TO_INCOME"]=(data["AMT_CREDIT"]+data["CB_AMT_CREDIT_SUM"])/data["AMT_INCOME_TOTAL"]

median_imputer=SimpleImputer(strategy="median").set_output(transform="pandas")
data["AMT_GOODS_PRICE"]=median_imputer.fit_transform(data["AMT_GOODS_PRICE"].to_numpy().reshape(-1,1))

# FEATURE ENGINEERING
data["AMT_CREDIT_NORM"]=data["AMT_CREDIT"]/data["AMT_GOODS_PRICE"]
data["AMT_ANNUITY"]=(data["AMT_ANNUITY"]+data["CB_AMT_ANNUITY"])/data["AMT_INCOME_TOTAL"]
data["AMT_INCOME_TOTAL_NORM"]=data["AMT_INCOME_TOTAL"]/data["AMT_GOODS_PRICE"]

data["BORROWER_AGE"]=data["DAYS_BIRTH"].apply(np.abs)//365
data["BORROWER_SENIORITY"]=data["DAYS_EMPLOYED"].apply(np.abs)//365
data["BORROWER_FIDELITY"]=data["DAYS_REGISTRATION"].apply(np.abs)//365

for col in ["DAYS_LAST_PHONE_CHANGE","AMT_INCOME_TOTAL_NORM", "AMT_INCOME_TOTAL","AMT_CREDIT","AMT_ANNUITY","AMT_GOODS_PRICE",
            "BORROWER_AGE","BORROWER_SENIORITY","BORROWER_FIDELITY"]:
    show_conditionnal_density(data,col)
    
    
tested_numerical_variables=[
    "BORROWER_AGE","BORROWER_SENIORITY","BORROWER_FIDELITY","AMT_INCOME_TOTAL_NORM",
    "AMT_CREDIT_NORM", "AMT_INCOME_TOTAL","AMT_CREDIT",
    "AMT_ANNUITY","AMT_GOODS_PRICE",
    'CB_AMT_CREDIT_SUM_DEBT', 'CB_NB_CREDIT_ACTIVE', 'CB_NB_CREDIT_CLOSED', 'CB_DAYS_CREDIT', 'CB_DAYS_CREDIT_ENDDATE', 'CB_AMT_CREDIT_SUM', 'CB_AMT_ANNUITY'
] 

for col in tested_numerical_variables:
    mannwhitney_test(data,col,"TARGET")
    
    
# echantillon d'entrainement et echantillon de calibrage
data_train, data_test=train_test_split(data, test_size=0.3, stratify=data["TARGET"], random_state=42)

discretised_cols=["AMT_INCOME_TOTAL_NORM", "AMT_CREDIT_TO_INCOME" , "BORROWER_AGE", "BORROWER_SENIORITY",
                  "BORROWER_FIDELITY", "AMT_CREDIT_NORM", "DAYS_LAST_PHONE_CHANGE"
                  ]
discretised_cols_2=["AMT_ANNUITY","AMT_GOODS_PRICE", "CB_DAYS_CREDIT",
                  'CB_AMT_CREDIT_SUM_DEBT', 'CB_NB_CREDIT_CLOSED', 
                  'CB_DAYS_CREDIT_ENDDATE', 'CB_AMT_CREDIT_SUM', 'CB_AMT_ANNUITY'
]

dt_discretizer=DecisionTreeDiscretizer(target=data_train["TARGET"]) #instanciation du discrétiseur

for col in discretised_cols:
    dt_discretizer.fit(data_train[col])
    data_train[col]=dt_discretizer.transform(data_train[col])
    data_test[col]=dt_discretizer.transform(data_test[col])
    

for col in discretised_cols_2:
    dt_discretizer.fit(data_train[col])
    data_train[col]=dt_discretizer.transform(data_train[col])
    data_test[col]=dt_discretizer.transform(data_test[col])
    
    
for col in discretised_cols+discretised_cols_2:
    show_risk_stability_overtime(data_train,col)
    
for col in discretised_cols+discretised_cols_2:
    show_volume_stability_overtime(data_train,col)
    
print("Calcul de l'Information value pour les variables discrétisées")
for col in discretised_cols+discretised_cols_2:
    print(f"{col} : {calculate_information_value_from_contingency_table(pd.crosstab(data_train['TARGET'], data_train[col]))}")
    print(60*"=")
    
    
# Modélisation 
print("Phase de modélisation")
formula="TARGET ~ C(OCCUPATION_TYPE,Treatment(reference=0)) + C(NAME_EDUCATION_TYPE,Treatment(reference='Non graduated'))  + C(AMT_CREDIT_NORM,Treatment(reference=3)) + C(BORROWER_AGE,Treatment(reference=0)) + C(BORROWER_SENIORITY,Treatment(reference=0)) + C(CB_NB_CREDIT_CLOSED, Treatment(reference=0))+ C(CB_DAYS_CREDIT,Treatment(reference=2)) - 1" # + C(DAYS_LAST_PHONE_CHANGE, Treatment(reference=3)) + C(FAM_STATS_CHILD,Treatment(reference='Single')) + +BORROWER_FIDELITY 
model_logit=sm.Logit.from_formula(formula=formula,data=data_train).fit()

print(model_logit.summary())

print("Performance sur le train")
y_train_proba=model_logit.predict(data_train)
gini=2*roc_auc_score(data_train["TARGET"],y_train_proba) - 1
print(f"{gini = :.3f}")


print("Performance sur le test")
y_test_proba=model_logit.predict(data_test)
gini=2*roc_auc_score(data_test["TARGET"],y_test_proba) - 1
print(f"{gini = :.3f}")