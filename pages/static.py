#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  4 18:27:01 2023

@author: leo
"""

# DASH 1 -Scatter Plot
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash
import plotly.express as px

# connecting the page to the app.py file
dash.register_page(__name__, path='/page-1', name='Static')


df = pd.read_csv('yu-gi-oh.csv')
df2 = df.query('type_short == "Monster"')


def pie_chart():
    df_pie = df[(df['type_short'] == 'Monster') | (df['type_short'] == 'Spell Card') | (df['type_short'] == 'Trap Card')]
    df1 = df_pie['type_short'].value_counts().reset_index()
    names = df1['index'].values
    values = df1['type_short'].values
    colors = ['blue', 'red', 'green']
    fig = px.pie(values=values, names=names, title='Population of Pokemon Generations', color_discrete_map=dict(colors=colors))
    return fig


def histogram():
    df3 = df[df['type_short'] == 'Monster'][['frameType', 'attribute']]
    fig = px.histogram(df3, x='attribute', color='frameType', nbins=len(df['attribute'].unique()), histfunc='count', barmode='stack')
    fig.update_layout(
    plot_bgcolor='#FFFFFF'
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')
    return fig


layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div([
            html.H2('Pie Chart'),
            html.Div([
                html.P('This pie chart shows the proportion of monster, spell and trap cards that are present in our dataset. '
                       'As you can see the monster cards are the most, they will be very helpful because you will need them'
                       ' to choose the attribute that will be at the base of your deck construction')
                ])
        ]))]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=pie_chart()), width=6)
    ], justify='center'),
    dbc.Row([
        dbc.Col(html.Div([
            html.H2('Histogram'),
            html.Div([
                html.P('This histogram shows how many cards are in the dataset'
                       ' according to each attribute that a monster card can have.'
                       ' Moreover can be seen that the different columns are colored'
                       ' with different colors. They shows the different type the monsters card belong to')
                ])
        ]))]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=histogram()), width=12)
    ]),
], fluid=True)





