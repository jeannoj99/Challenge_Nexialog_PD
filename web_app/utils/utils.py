# En gros c'est pour les fonctions qu'on appellera plusieurs fois (pas des callbacks)

import plotly.graph_objects as go
import pandas as pd
from scipy.stats import mannwhitneyu ,chi2_contingency
import numpy as np

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
                      legend_title=colname)
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
        legend_title=colname
    )
    return fig

def convert_numeric_to_category(df: pd.DataFrame):
    for colname in df.columns.tolist():
        if (df[colname].dtype=="number") & (df[colname].nunique() <=10):
            df[colname]=df[colname].astype("category")
            pass
        else:
            pass

def cramers_v(data,col):
    contingency_table=pd.crosstab(data["TARGET"], data[col])
    chi2 = chi2_contingency(contingency_table)[0]
    n = contingency_table.sum().sum()
    phi2 = chi2 / n
    r, k = contingency_table.shape
    phi2corr = max(0, phi2 - ((k-1)*(r-1))/(n-1))
    rcorr = r - ((r-1)**2)/(n-1)
    kcorr = k - ((k-1)**2)/(n-1)
    return f"cramers V: {round(np.sqrt(phi2corr / min((kcorr-1), (rcorr-1))),3)}"


def mannwhitney_test(df: pd.DataFrame, variable: str):
    if df[variable].dtype not in ['int64', 'float64']: 
        return f"{variable} n'est pas numérique"

    group_1 = df[df["TARGET"] == 0]
    group_2 = df[df["TARGET"] == 1]

    stat, p_value = mannwhitneyu(group_1[variable].dropna(), group_2[variable].dropna())
    return f"Pour {variable}, Mann-Whitney U-Statistic: {round(stat, 3)} (p-value: {round(p_value, 3)})"


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

def calculate_chi_stat(data,col):
    contingency_table=pd.crosstab(data["TARGET"], data[col])
    chi2, p, _, _ = chi2_contingency(contingency_table, correction=True)     
    return f"Chi-squared: {round(chi2,2)} (p-value: {round(p,3)})"