# DASH 1 -Scatter Plot
from dash import Dash, dcc, Output, Input  # pip install dash
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import plotly.express as px
import pandas as pd   
import dash
from dash import Dash, html, dcc, callback


df=pd.read_csv('yu-gi-oh.csv')
df2=df.query('type_short=="Monster"')

# connecting the page to the app.py file
dash.register_page(__name__, path='/page-2', name='Scatter Plot for monsters')


# components
mytitle = dcc.Markdown(children='')
mygraph = dcc.Graph(figure={})

# rangeslider for price
rangeslider = dcc.RangeSlider(
    min=0, max=100, step=10, value=[0, 100], id='my-range-slider')

# dropdown menu for attribute
dropdown2 = dcc.Dropdown(options=['EARTH', 'WATER', 'WIND', 'DARK', 'LIGHT', 'FIRE', 'DIVINE'], # assigning the posssible values thta we want to show on the dropdown menu
                        value=['EARTH', 'WATER'],  # initial value displayed when page first loads
                        multi=True,
                        clearable=False,
                        className="dcc_control")

#dropdown menu fro type
dropdown = dcc.Dropdown(options=['effect', 'normal', 'xyz', 'fusion'], # assigning the posssible values thta we want to show on the dropdown menu
                        value='effect',  # initial value displayed when page first loads
                        clearable=False)
# Customize your own Layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div([
            html.H2('Scatter Plot'),
            html.Div([
                html.P('In this section can be seen a scatter plot with the attack '
                       'variable on the x and the defense on the y. You can choose'
                       ' which type of monster to see and compare them according '
                       'to their attribute. Moreover you can use the slide bar to '
                       'select the range of price of the cards. You will have the '
                       'possibility to compare the monsters cards and you will be '
                       'able to choose if you want a deck that is more defensive,'
                       ' more offensive or with cheaper cards. Choose an attribute twhere to build your deck on and if after using this'
                       ' graph you have still doubt you can comopare the monsters'
                       ' card using the next plot.')
                ])
        ]))]),
    dbc.Row([
        dbc.Col([mygraph], width=12)
    ]),
    dbc.Row([
        dbc.Col([html.Label('Monster Attribute'), dropdown2], width=6)
    ], justify='left'),
    dbc.Row([
        dbc.Col([html.Label('Monster Type'), dropdown], width=6),
        dbc.Col([html.Label('Price Range'), rangeslider], width=6)
    ], justify='between'),
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
    Input(dropdown2, 'value'),
    Input(rangeslider, 'value')
)
def update_graph(frame, attribute, price_range):  
    
    
    # filtering the dataframe according to the informations given as input
    filtered_df = df2.loc[(df2['frameType']==frame)&
                          (df2['attribute'].isin(attribute))&
                          (df2['cardmarket_price'] >= price_range[0])&
                          (df2['cardmarket_price'] <= price_range[1])]
    # scatter plot
    fig = px.scatter(filtered_df, x="atk", y="def",
                     color= 'attribute', 
                     hover_data=['name'])
    # scatter plot layout
    fig.update_layout(
    plot_bgcolor='#FFFFFF'
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey', range=[0, 5000])
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey', range=[0, 5000])

    return fig

