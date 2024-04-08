import os
import sys
import pickle
import pandas as pd
path=os.getcwd()
sys.path.append(path+"/..")

from src.score import grid_score, attribute_score, attribute_chr, subplot_segment_default_rate

required_columns={
    "Cash" : [],
    "Revolving" : []
}

discretizers={
    "Cash": None,
    "Revolving" : None
}   # a mettre des dictionnaires qui pour chaque variable a le discretiseur entrainé

breaks = {
    "Cash" : pickle.load("../utils/Cash/breaks.pkl"),
    "Revolving" : pickle.load("../utils/Revolving/breaks.pkl")
}



class Dataset:
    
    def __init__(self,data : dict) -> None:
        self.data = pd.DataFrame(data)
        self.contract_type = data["NAME_CONTRACT_TYPE"]
        self.discretizers = discretizers[self.contract_type]
        self.required_columns = required_columns[self.contract_type]
        self.note_breaks = breaks[self.contract_type]
    
    def check_columns(self):
        if len(set(self.required_columns).difference(self.data.columns)) == 0:
            return True
        else :
            return False
        
        
    def transform_columns(self):
        if self.check_columns():
            pass
        else:
            pass
    
    def get_chr(self):
        self.transform_columns()
        score = attribute_score(grid_score=None, data=self.data)
        segment = attribute_chr(score.values, threshold=self.note_breaks)
        return
    
    
class ExpertSystem (Dataset):
    
    def __init__(self,data:Dataset) :
        self.data = data
        
    def get_decision(self):
        segment = self.data.get_chr()
        if segment in [5,6]:
            return "Approval"
        elif segment in [2,3,4]:
            return "Referal to Analyst"
        elif segment in [0,1]:
            return "Refusal"
        else :
            return None
    
        
        
