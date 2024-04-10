# En gros c'est pour les fonctions qu'on appellera plusieurs fois (pas des callbacks)

import plotly.graph_objects as go
import pandas as pd


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