
import plotly.graph_objects as go
import pandas as pd
from scipy.stats import mannwhitneyu ,chi2_contingency, kruskal
import numpy as np
from sklearn.tree import DecisionTreeClassifier

def show_risk_stability_graph(data: pd.DataFrame, colname):
    result = data.groupby([colname, "date_annee"])['TARGET'].value_counts(normalize=True).unstack().fillna(0)[1]
    fig = go.Figure()
    for col_value, values in result.groupby(level=0):
        fig.add_trace(go.Scatter(x=values.index.get_level_values("date_annee"),
                                 y=values.values,
                                 mode='lines+markers',
                                 name=col_value,
                                 hovertemplate="Année: %{x}<br>Taux de défaut: %{y:.3f}"))

    fig.update_layout(title=f"Stabilité en risque de {colname}",
                      xaxis_title='date_annee',
                      yaxis_title='Taux de défaut',
                      legend_title=colname,
                      template = "simple_white")
    return fig

def show_volume_stability_overtime(data:pd.DataFrame, colname:str, threshold=0.05):
    resultats = data[[colname, "date_annee"]].groupby(by=["date_annee"]).value_counts(normalize=True).unstack().fillna(0)
    fig = go.Figure()
    for col_value in resultats.columns:
        fig.add_trace(go.Scatter(
            x=resultats.index,
            y=resultats[col_value],
            mode='lines+markers',
            name=col_value
        ))
    fig.add_hline(y=threshold, line_dash="dash")
    fig.update_layout(
        title=f'Stabilité en volume de {colname}',
        xaxis_title='Temps',
        yaxis_title='Pourcentage',
        legend_title=colname,
        template = "simple_white"
    )
    return fig

def convert_numeric_to_category(df: pd.DataFrame):
    for colname in df.columns.tolist():
        if (df[colname].dtype=="number") & (df[colname].nunique() <=10):
            df[colname]=df[colname].astype("category")
            pass
        else:
            pass

def cramers_v_target(data,col):
    contingency_table=pd.crosstab(data["TARGET"], data[col])
    chi2 = chi2_contingency(contingency_table)[0]
    n = contingency_table.sum().sum()
    phi2 = chi2 / n
    r, k = contingency_table.shape
    phi2corr = max(0, phi2 - ((k-1)*(r-1))/(n-1))
    rcorr = r - ((r-1)**2)/(n-1)
    kcorr = k - ((k-1)**2)/(n-1)
    return f"cramers V: {round(np.sqrt(phi2corr / min((kcorr-1), (rcorr-1))),3)}"

def cramers_v_cols(data,col1,col2):
    contingency_table=pd.crosstab(data[col1], data[col2])
    chi2 = chi2_contingency(contingency_table)[0]
    n = contingency_table.sum().sum()
    phi2 = chi2 / n
    r, k = contingency_table.shape
    phi2corr = max(0, phi2 - ((k-1)*(r-1))/(n-1))
    rcorr = r - ((r-1)**2)/(n-1)
    kcorr = k - ((k-1)**2)/(n-1)
    return f"cramers V: {round(np.sqrt(phi2corr / min((kcorr-1), (rcorr-1))),3)}"


def kruskal_wallis_test(df: pd.DataFrame, variable: str):
    if df[variable].dtype not in ['int64', 'float64']: 
        return f"{variable} n'est pas numérique"

    group_1 = df[df["TARGET"] == 0]
    group_2 = df[df["TARGET"] == 1]

    stat, p_value = kruskal(group_1[variable].dropna(), group_2[variable].dropna())
    return f"Pour {variable}, Kruskal-Wallis Statistic: {round(stat, 3)} (p-value: {round(p_value, 3)})"


def calculate_information_value(data,col):
    contingency_table=pd.crosstab(data["TARGET"], data[col])
    """_summary_

    Args:
        contingency_table (pd.DataFrame): Tableau croisée dynamique du prédicteur catégoriel et de la target

    Returns:
        float: _description_
    """
    non_event_rate=contingency_table.iloc[0]/(contingency_table.iloc[0].sum())
    event_rate=contingency_table.iloc[1]/(contingency_table.iloc[1].sum())
    iv=0
    if (non_event_rate.min() > 0) & (event_rate.mean() >0) :
        for col in non_event_rate.index:
            iv += (event_rate[col] - non_event_rate[col])*np.log(event_rate[col] / non_event_rate[col])

    return f"Information value: {round(iv,4)}"

def calculate_chi_stat_target(data,col):
    contingency_table=pd.crosstab(data["TARGET"], data[col])
    chi2, p, _, _ = chi2_contingency(contingency_table, correction=True)     
    return f"Chi-squared: {round(chi2,2)} (p-value: {round(p,3)})"

def calculate_chi_stat_cols(data,col1,col2):
    contingency_table=pd.crosstab(data[col1], data[col2])
    chi2, p, _, _ = chi2_contingency(contingency_table, correction=True)     
    return f"Chi-squared: {round(chi2,2)} (p-value: {round(p,3)})"

def grid_score(data_train,results_model_logit, variables_utilisees) -> pd.DataFrame:
    index_logit = list(results_model_logit.params.index)

    variables_logit = []
    modalites_variables = []

    # récupérer les variables
    for ligne in index_logit :
        variable = ligne.split(",")[0].replace("C(","")
        variables_logit.append(variable)

        modalite = ligne.split("[")[-1].replace("]","")
        if "T.Interval" in modalite :
            modalite = modalite.replace("T.Interval","")
        if ", closed='right'" in modalite :
            modalite = modalite.replace(", closed='right')", "]")
        if "T." in modalite :
            modalite = modalite.replace("T.","")
        modalites_variables.append(modalite)

    df_coef = pd.DataFrame({'Variable': variables_logit, 'Modalités': modalites_variables, 'Coefficient' : list(results_model_logit.params), 'p-value' : list(results_model_logit.pvalues)})

    # variables_utilisees = ["OCCUPATION_TYPE", "NAME_EDUCATION_TYPE"  , "AMT_CREDIT_NORM" , "BORROWER_AGE" , "BORROWER_SENIORITY" , "CB_NB_CREDIT_CLOSED", "CB_DAYS_CREDIT"]
    grid = {'Variable':[],'Modalités':[],'effectif':[],}

    for var in variables_utilisees:
        for modalite in data_train[var].value_counts().reset_index()[var].unique():
            grid['Variable'].append(var)
            grid['Modalités'].append(modalite)
            effectif_pct = data_train[var].value_counts(normalize=True)[modalite] 
            grid['effectif'].append(effectif_pct)
    grid=pd.DataFrame(grid)
    grid['Modalités'] =grid['Modalités'].apply(str) #màj ici
    grid['Coefficient']=0

    grid_df=pd.merge(grid.drop(columns='Coefficient'),df_coef, on=['Variable', 'Modalités'], how='outer')
    grid_df=grid_df.pivot_table(index=['Variable', 'Modalités'], values=['effectif', 'Coefficient', 'p-value'], aggfunc='sum')
    grid_df=grid_df.reset_index()
    grid_df['Modalités'] =grid_df['Modalités'].apply(str)

    grid_df = grid_df.drop_duplicates(subset=['Variable','Modalités'],keep='last').reset_index(drop=True)

    notes = []
    sum_diff = sum([coefficients.max() - coefficients.min() for variable, coefficients in grid_df.groupby('Variable')['Coefficient']])

    #chaque ligne du DataFrame
    for index, row in grid_df.iterrows():
        # Extraire la variable correspondante à la modalité
        variable = row['Variable']
        
        coefficients_variable = grid_df.loc[grid_df['Variable'] == variable, 'Coefficient']
        note = 1000 * ((coefficients_variable.max() - row['Coefficient']) / sum_diff)
        notes.append(note)


    grid_df['Note'] = notes

    for var in grid_df['Variable'].unique():
        for modal in grid_df[grid_df['Variable'] == var]['Modalités'].unique():
            tmp = data_train[var].value_counts(normalize=True)
            proportion = tmp[tmp.index.astype(str) == modal].iloc[0]
            grid_df.loc[(grid_df['Variable'] == var) & (grid_df['Modalités'] == modal), 'effectif'] = proportion


    moyennes= {}
    contributions = []
    for var in grid_df['Variable'].unique():
        moyennes[var] = grid_df[grid_df['Variable']==var]['Note'].mean()
        
    denominator = np.sum([np.sqrt(np.sum([(row['effectif'] * (row['Note'] - moyennes[var])**2) for _, row in grid_df.loc[grid_df['Variable'] == var].iterrows()])) for var in grid_df['Variable'].unique()])

    for index, row in grid_df.iterrows():
        variable = row['Variable']
        mean_note = moyennes[variable]
        #formule
        numerator = np.sqrt(np.sum([(row['effectif'] * (row['Note'] - mean_note)**2) for _, row in grid_df.loc[grid_df['Variable'] == variable].iterrows()]))
        contribution = numerator / denominator
        contributions.append(contribution*100)


    grid_df['Contribution'] = contributions

    tx_df = {'Variable':[],'Modalités':[],'tx_defaut':[]}
    for var in grid_df['Variable'].unique():
        for modalite in grid_df[grid_df['Variable']==var]['Modalités'].unique():

            defauts = data_train[data_train[var].apply(str)==modalite]['TARGET'].sum()
            tout_lemonde =  data_train[data_train[var].apply(str)==modalite]['TARGET'].shape[0]
            tx_defaut= defauts/tout_lemonde * 100
            tx_df['Variable'].append(var)
            tx_df['Modalités'].append(modalite)
            tx_df['tx_defaut'].append(tx_defaut)

    tx_df= pd.DataFrame(tx_df)
    Grille_score = pd.merge(grid_df, tx_df, on=['Variable', 'Modalités'], how='left')
    Grille_score['Contribution'] = Grille_score['Contribution'].apply(lambda row: round(row,2))
    Grille_score['Note'] = Grille_score['Note'].apply(lambda row: round(row))
    Grille_score['tx_defaut'] = Grille_score['tx_defaut'].apply(lambda row: round(row,2))
    Grille_score['Coefficient'] = Grille_score['Coefficient'].apply(lambda row: round(row,4))
    Grille_score['p-value'] = Grille_score['p-value'].apply(lambda row: round(row,3))
    Grille_score['effectif'] = Grille_score['effectif'].apply(lambda row: round(row*100,1))

    return Grille_score


def attribute_score(grid_score, data):
    data['Note'] = 0  
    for var in grid_score["Variable"].unique():
        modal = grid_score[grid_score['Variable'] == var]['Modalités'].unique()
        for i in range(len(modal)):
            condition = data[var].apply(str) == modal[i]  # Condition pour vérifier la modalité
            note = grid_score[(grid_score['Variable'] == var) & (grid_score['Modalités'] == str(modal[i]))]['Note'].values[0]
            data['Note'] = np.where(condition, data['Note'] + note, data['Note'])
    pass

class DecisionTreeDiscretizer:
    def __init__(self, max_bins=5, target=None):
        self.tree_max_bins = max_bins
        self.clf = DecisionTreeClassifier(criterion="gini", max_depth=int(round(self.tree_max_bins/2)),
                                          min_samples_split=0.05,
                                           min_samples_leaf=0.05) #
        self.target = target

    def fit(self, X_train):
        # Entraîner le modèle sur les données d'entraînement
        self.clf.fit(X_train.values.reshape(-1, 1), self.target)

    def _get_tree_thresholds(self):
        thresholds = set()
        for node in range(self.clf.tree_.node_count):
            if self.clf.tree_.children_left[node] != self.clf.tree_.children_right[node]:  # non-leaf node
                feature = self.clf.tree_.feature[node]
                threshold = self.clf.tree_.threshold[node]
                thresholds.add(threshold)
        return np.array(list(thresholds))

    def get_thresholds(self):
        if hasattr(self.clf, 'tree_') and self.clf.tree_ is not None:
            thresholds_np = self._get_tree_thresholds()
            thresholds = [-np.inf] + sorted(list(set(list(thresholds_np)))) + [np.inf]
            return thresholds
        else:
            raise ValueError("Le classifieur n'est pas entraîné. Utilisez la méthode fit avant d'obtenir les seuils.")

    def transform(self, X):
        # Vérifier si le modèle est entraîné
        if not hasattr(self.clf, 'tree_') or self.clf.tree_ is None:
            raise ValueError("Le classifieur n'est pas entraîné. Utilisez la méthode fit avant de transformer les données de test.")

        thresholds = self.get_thresholds()

        # Utiliser pd.cut pour obtenir les intervalles au lieu des numéros
        intervals = pd.cut(X.values.flatten(), bins=thresholds, include_lowest=True, right=True)
        return intervals
    
def attribute_chr(score,threshold):
    return pd.cut(score, bins=threshold, labels=[i for i in range(len(threshold))])