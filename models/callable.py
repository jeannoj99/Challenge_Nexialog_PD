import os
import sys
import pickle
import numpy as np
import pandas as pd
import openpyxl
path=os.getcwd()
sys.path.append(path+"")
from src.preprocessing import DecisionTreeDiscretizer
from src.score import grid_score, attribute_score, attribute_chr, subplot_segment_default_rate

required_columns={
    "Cash loans" : ["OCCUPATION_TYPE", "NAME_EDUCATION_TYPE" , "CB_NB_CREDIT_CLOSED",
              "CB_DAYS_CREDIT", "AMT_CREDIT","CB_AMT_CREDIT_SUM","AMT_INCOME_TOTAL",
              "AMT_GOODS_PRICE","DAYS_BIRTH", "DAYS_EMPLOYED", "DAYS_REGISTRATION" ],
    "Revolving loans" : ["OCCUPATION_TYPE", "NAME_EDUCATION_TYPE" , "CB_NB_CREDIT_CLOSED",
              "CB_DAYS_CREDIT", "AMT_CREDIT","CB_AMT_CREDIT_SUM","AMT_INCOME_TOTAL",
              "AMT_GOODS_PRICE","DAYS_BIRTH", "DAYS_EMPLOYED", "DAYS_REGISTRATION" ]
}

cash_grid_score=pd.read_excel("data/grille_de_score.xlsx", index_col=0)
revolving_grid_score = pd.read_excel("data/grille_de_score_revolving.xlsx", index_col=0)

discretizers={}

with open("utils/Revolving/discretizers.pkl", "rb") as f:
    discretizers["Revolving loans"]=pickle.load(f)

with open("utils/Cash/discretizers.pkl", "rb") as f:
    discretizers["Cash loans"]=pickle.load(f)

breaks = {}

with open("utils/Cash/breaks.pkl", "rb") as f:
    breaks["Cash loans"]=pickle.load(f)

with open("utils/Revolving/breaks.pkl", "rb") as f:
    breaks["Revolving loans"]=pickle.load(f)

class DecisionExpertSystem :

    def __init__(self,data : dict) -> None:
        self.data = pd.DataFrame(data, index=[0])
        self.contract_type = data["NAME_CONTRACT_TYPE"]
        # self.get_attributes()
        self.discretizers = discretizers[self.contract_type]
        self.required_columns = required_columns[self.contract_type]
        self.note_breaks = breaks[self.contract_type]
        self.cash_scorecard = cash_grid_score   
        self.revolving_scorecard = revolving_grid_score
    
  
    
    def get_attributes(self):
        self.discretizers = discretizers[self.contract_type]
        self.required_columns = required_columns[self.contract_type]
        self.note_breaks = breaks[self.contract_type]
        self.cash_scorecard = cash_grid_score   
        self.revolving_scorecard = revolving_grid_score
        pass
     
    group_education_type={
    "Graduated" : ["Academic degree", "Higher education"],
    "Non graduated":["Lower secondary", "Secondary / secondary special", "Incomplete higher"]
}
    group_occupation_type = {
        "Cash loans":{
    0: ['Accountants', 'HR staff', 'High skill tech staff'],
 1: ['Managers', 'Core staff', 'Private service staff', 'Unknown',
        'Medicine staff', 'IT staff', 'Secretaries'],
 2: ['Realty agents', 'Cleaning staff', 'Sales staff', 'Laborers',
        'Cooking staff', 'Security staff'],
 3: ['Drivers', 'Waiters/barmen staff', 'Low-skill Laborers'],
},
        "Revolving loans" : {
       0: ['IT staff', 'Accountants', 'HR staff', 'Managers', 'High skill tech staff', 'Core staff'], 
       1: ['Unknown', 'Medicine staff', 'Private service staff'],
       2: ['Realty agents', 'Secretaries', 'Laborers', 'Security staff',
              'Sales staff', 'Drivers', 'Waiters/barmen staff', 'Cleaning staff',
              'Cooking staff', 'Low-skill Laborers']
}
    }
    
    def check_columns(self):
        if len(set(self.required_columns).difference(self.data.columns)) == 0:
            return True
        else :
            return False
        
        # mettre des valeurs par défaut pour ne pas avoir à imputer
    
    def _features_tranformation(self):
        self.data["NAME_EDUCATION_TYPE"] = self.data["NAME_EDUCATION_TYPE"].map({value: key for key, values in self.group_education_type.items() for value in values})
        self.data["OCCUPATION_TYPE"] = self.data["OCCUPATION_TYPE"].map({value: key for key, values in self.group_occupation_type[self.contract_type].items() for value in values})
        
        if self.contract_type == "Cash loans":
            # ['BORROWER_AGE', 'BORROWER_SENIORITY', 'AMT_CREDIT_NORM', 'CB_NB_CREDIT_CLOSED', 'CB_DAYS_CREDIT']
            
            self.data['BORROWER_AGE']=self.discretizers['BORROWER_AGE'].transform(self.data['BORROWER_AGE'])
            self.data['BORROWER_SENIORITY']=self.discretizers['BORROWER_SENIORITY'].transform(self.data['BORROWER_SENIORITY'])
            self.data['AMT_CREDIT_NORM']=self.discretizers['AMT_CREDIT_NORM'].transform(self.data['AMT_CREDIT_NORM'])
            self.data['CB_NB_CREDIT_CLOSED']=self.discretizers['CB_NB_CREDIT_CLOSED'].transform(self.data['CB_NB_CREDIT_CLOSED'])
            self.data['CB_DAYS_CREDIT']=self.discretizers['CB_DAYS_CREDIT'].transform(self.data['CB_DAYS_CREDIT'])
            
            pass
        elif self.contract_type =="Revolving loans":
            self.data['BORROWER_AGE']=self.discretizers['BORROWER_AGE'].transform(self.data['BORROWER_AGE'])
            self.data['BORROWER_SENIORITY']=self.discretizers['BORROWER_SENIORITY'].transform(self.data['BORROWER_SENIORITY'])
            self.data['AMT_CREDIT_NORM']=self.discretizers['AMT_CREDIT_NORM'].transform(self.data['AMT_CREDIT_NORM'])
            self.data['CB_NB_CREDIT_CLOSED']=self.discretizers['CB_NB_CREDIT_CLOSED'].transform(self.data['CB_NB_CREDIT_CLOSED'])
            self.data['CB_DAYS_CREDIT']=self.discretizers['CB_DAYS_CREDIT'].transform(self.data['CB_DAYS_CREDIT'])
            pass
        
    def transform_columns(self):
        
        if self.check_columns():

            self.data["AMT_CREDIT_TO_INCOME"]=(self.data["AMT_CREDIT"] + self.data["CB_AMT_CREDIT_SUM"])/self.data["AMT_INCOME_TOTAL"]

            # median_imputer=SimpleImputer(strategy="median").set_output(transform="pandas")
            # self.data["AMT_GOODS_PRICE"]=median_imputer.fit_transform(self.data["AMT_GOODS_PRICE"].to_numpy().reshape(-1,1))
            
            self.data["AMT_CREDIT_NORM"]=self.data["AMT_CREDIT"]/self.data["AMT_GOODS_PRICE"]
            # self.data["AMT_ANNUITY"]=(self.data["AMT_ANNUITY"]+self.data["CB_AMT_ANNUITY"])/self.data["AMT_INCOME_TOTAL"]
            self.data["AMT_INCOME_TOTAL_NORM"]=self.data["AMT_INCOME_TOTAL"]/self.data["AMT_GOODS_PRICE"]
            self.data["BORROWER_AGE"]=self.data["DAYS_BIRTH"].apply(np.abs)//365
            self.data["BORROWER_SENIORITY"]=self.data["DAYS_EMPLOYED"].apply(np.abs)//365
            self.data["BORROWER_FIDELITY"]=self.data["DAYS_REGISTRATION"].apply(np.abs)//365
            self._features_tranformation()
            
        else:
            pass
        
    def score(self):
        if self.contract_type == "Cash loans":
            attribute_score(grid_score=self.cash_scorecard, data=self.data)
            pass
        elif self.contract_type == "Revolving loans":
            attribute_score(grid_score=self.revolving_scorecard, data=self.data)
            pass
    
    def get_chr(self):
        self.score()
        score = self.data["Note"].values[0]
        # segment = attribute_chr(score, threshold=self.note_breaks)
        for i in range(len(self.note_breaks)-1):
            if (score >= self.note_breaks[i]) & (score < self.note_breaks[i+1]):
                return i
            else:
                pass
        
    
    def get_decision(self):
        segment = self.get_chr()
        
        if segment in [5,6]:
            return "Approval","green"
        elif segment in [2,3,4]:
            return "Referal to Analyst","yellow"
        elif segment in [0,1]:
            return "Refusal","red"
        else :
            return None
    

    
# test={'NAME_CONTRACT_TYPE': 'Cash loans', 'OCCUPATION_TYPE': 'Drivers', 'NAME_EDUCATION_TYPE': 'Secondary / secondary special', 'CB_NB_CREDIT_CLOSED': 0, 'CB_DAYS_CREDIT': 0, 'AMT_CREDIT': 0, 'CB_AMT_CREDIT_SUM': 0, 'AMT_INCOME_TOTAL': 0, 'AMT_GOODS_PRICE': 0, 'DAYS_BIRTH': 365*35, 'DAYS_EMPLOYED': 0, 'DAYS_REGISTRATION': 0}      

   
# system = DecisionExpertSystem(test)

# system.transform_columns()
# system.score()
# print(system.get_decision())

