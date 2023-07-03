# DASH 2 - BoxPlot
from dash import Dash, dcc, Output, Input  # pip install dash
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import plotly.graph_objects as go
import pandas as pd   
#from pyvis.network import Network
import dash
from dash import Dash, html, dcc, callback

df=pd.read_csv('yu-gi-oh.csv')
df2=df.query('type_short=="Monster"')

# components

# connecting the page to the app.py file
dash.register_page(__name__, path='/page-3', name='Box Plot for monster atk, def and level')

mytitle = dcc.Markdown(children='')
mygraph = dcc.Graph(figure={})

# setting the dropdown menu
dropdown = dcc.Dropdown(options=df2['attribute'].unique(), # assigning the posssible values thta we want to show on the dropdown menu
                        value=['EARTH', 'WATER'],
                        multi=True,
                        clearable=False)
# setting the radio botton
radio_botton= dcc.RadioItems(
   options=['atk', 'def', 'level'],
   value='atk'
)

# Customize your own Layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div([
            html.H2('Box Plot'),
            html.Div([
                html.P("If the previous graph didn't help you enough you can"
                       " use this box plot to compare again the different monster cards."
                       " You will be able to select if you want to compare them "
                       "according to their attack, their defense or their level."
                       " Choosing an attribute among the one proposed is so important"
                       " to build your perfect deck. Once choosen an attribute go to"
                       " the next page so you'll be able to choose also your spell "
                       "and trap card to complete your deck")
                ])
        ]))]),
    dbc.Row([
        dbc.Col([mytitle], width=6)
    ], justify='center'),
    dbc.Row([
        dbc.Col([mygraph], width=12)
    ]),
    dbc.Row([
        dbc.Col([html.Label('Monster Attribute'), dropdown], width=6),
        dbc.Col([html.Label('Feature'), radio_botton], width=6)
    ], justify='left'),
    dbc.Row([
        dbc.Col([
            html.Div(style={'height': '100px'})
            ])
        ], justify='center')
], fluid=True)


# set the callback
@callback(
    Output(mygraph, 'figure'),
    Input(dropdown, 'value'),
    Input(radio_botton, 'value')
)
def update_graph(attribute, feature):  
    
    
    # filtering the dataframe accroding to the information given as input by the user
    filtered_df = df2.loc[df2['attribute'].isin(attribute)]
    
    # defining the boxplot
    fig=go.Figure()
    for elem in filtered_df['attribute'].unique():
        fig.add_trace(go.Box(x=filtered_df[filtered_df['attribute']==elem][feature],
                             name=elem,
                             boxpoints='all',
                             jitter=0.3,
                             pointpos=0.5))
        # updating the layout
        fig.update_layout(xaxis_title=feature,
                              yaxis_title='Attribute',
                              plot_bgcolor='#FFFFFF')
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')
    
    
        
    
    return fig
