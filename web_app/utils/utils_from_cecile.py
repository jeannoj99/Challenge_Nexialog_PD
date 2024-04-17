import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
from jenkspy import JenksNaturalBreaks
import plotly.express as px
from dash import dash_table
import plotly.graph_objects as go
import dash_mantine_components as dmc



def subplot_segment_default_rate(data):
    mean_target_by_segment = data.groupby('Segment')['TARGET'].mean().reset_index()
    
    color_scale = []

    for segment, default_rate in zip(mean_target_by_segment['Segment'], mean_target_by_segment['TARGET']):
        if default_rate < 0.03:
            color_scale.append('green') 
        elif default_rate < 0.1:
            color_scale.append('#F1F74B')  
        else:
            color_scale.append('#DA3232')   

    # Create a dictionary to map segment to color
    segment_color_map = dict(zip(mean_target_by_segment['Segment'], color_scale))

    # Map the colors to the segments in the original order
    bar_colors = [segment_color_map[segment] for segment in data['Segment'].value_counts(normalize=True).index]

    fig = go.Figure()

    fig.add_trace(go.Bar(x=data['Segment'].value_counts(normalize=True).index,
                         y=data['Segment'].value_counts(normalize=True),
                         marker=dict(color=bar_colors),
                         showlegend=False))
    fig.add_trace(go.Scatter(x=mean_target_by_segment['Segment'],
                             y=mean_target_by_segment['TARGET'],
                             mode='lines+markers',
                             line=dict(color='navy', width=2),
                             yaxis='y2',
                             showlegend=False))
    
    fig.update_layout(annotations=[
        dict(
            x=0.5,
            y=1.15,
            xref='paper',
            yref='paper',
            text="Taux de défaut",
            showarrow=False,
            font=dict(color="navy",size=14)
        ),
        dict(
            x=0.15,
            y=1.05,
            xref='paper',
            yref='paper',
            text="Élevé",
            showarrow=False,
            font=dict(color="#DA3232", size=12)
        ),
        dict(
            x=0.5,
            y=1.05,
            xref='paper',
            yref='paper',
            text="Modéré",
            showarrow=False,
            font=dict(color="#F1F74B", size=12)
        ),
        dict(
            x=0.85,
            y=1.05,
            xref='paper',
            yref='paper',
            text="Faible",
            showarrow=False,
            font=dict(color="green", size=12)
        )

    ])

    fig.update_layout(xaxis=dict(title='Segment',tickmode='array', tickvals=mean_target_by_segment['Segment']),
                      yaxis=dict(title='Répartition par segment'),
                      yaxis2=dict(title='Taux de défaut', color='navy', overlaying='y', side='right'))
    
    return fig



def show_risk_stability_overtime(data: pd.DataFrame, colname: str):
    result = data.groupby([colname, "date_annee"])['TARGET'].value_counts(normalize=True).unstack().fillna(0)[1]
    fig = px.line(result, x=result.index.get_level_values("date_annee"),
                  y=result.values, color=result.index.get_level_values(f"{colname}"), markers=True)
    fig.update_layout(xaxis=dict(title="date_annee", type='category'),
                      yaxis_title="taux de défaut",
                      legend_title="Segment")
    return fig


def show_risk_stability_overtime_2(data: pd.DataFrame, colname: str):
    result = data.groupby([colname, "date_annee"])['TARGET'].mean().reset_index()
    fig = px.bar(result, x="Segment", y="TARGET", color=colname, barmode='group')
    fig.update_layout(xaxis=dict(title="Taux de défaut par segment pour l'année 2020", type='category'),
                      yaxis_title="Taux de défaut moyen",
                      legend_title="Segment")
    

    return fig



####################################################################################################################################
###################################################            JYNALDO              ################################################
####################################################################################################################################


def plot_feature_importances(model):
    
    # Obtenir les importances des features avec 'gain' comme mesure de l'importance
    importance = model.feature_importances_
    features_df = pd.DataFrame({
        'Feature': model.feature_names_in_,
        'Importance': importance
    }).sort_values(by='Importance', ascending=False)
    
    # Créer et retourner un graphique pour les features importances
    fig = px.bar(
        features_df, 
        x='Importance', 
        y='Feature', 
        orientation='h', 
        title='Représentation des Feature importances',
        labels={'Feature': 'Feature', 'Importance': 'Importance'},
        height=500,  # Hauteur du graphique
        width=700   # Largeur du graphique
    )
    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        plot_bgcolor='white',
        xaxis_title='Importance Score',
        yaxis_title='Features'
    )
    return fig
