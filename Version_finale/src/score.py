import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns




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


def subplot_segment_default_rate(data):
    mean_target_by_segment = data.groupby('Segment')['TARGET'].mean().reset_index()
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(data['Segment'].value_counts(normalize=True), color='lightblue', label='Distribution des Segments')
    ax2 = ax.twinx()
    sns.lineplot(x='Segment', y='TARGET', data=mean_target_by_segment, marker='o', color='red', linewidth=2, label='Taux de défaut')
    ax.set_ylabel('Taux d\'observations par segment', color='blue')
    ax2.set_ylabel('Taux de défaut', color='blue')
    plt.title('Répartition des CHR et des taux de défaut par CHR')
    plt.show()
    pass