# DASH 3 - BarChart

# DASH 2 - BoxPlot
from dash import Dash, dcc, Output, Input  # pip install dash
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import plotly.express as px
import pandas as pd   
#from pyvis.network import Network
import dash
from dash import Dash, html, dcc, callback

# importing the dataframe
df_exploded=pd.read_csv('df_exploded.csv')

# setting the variables that will be used for the color palette late rfor the garph
colorscales = px.colors.named_colorscales()
scale=colorscales[27]


# components

# connecting the page to the app.py file
dash.register_page(__name__, path='/page-4', name='Spell and trap card')

mytitle = dcc.Markdown(children='')
mygraph = dcc.Graph(figure={})

# setting the radio botton
radio_botton=dcc.RadioItems(
    options=['spell', 'trap'],
    value='spell'
    )
# setting the dropdown menu
dropdown = dcc.Dropdown(options=['DARK', 'LIGHT', 'EARTH', 'WIND', 'WATER', 'FIRE', 'DIVINE'], # assigning the posssible values thta we want to show on the dropdown menu
                        value='EARTH',  # initial value displayed when page first loads
                        clearable=False)

# Customize your own Layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div([
            html.H2('Spell and Trap card'),
            html.Div([
                html.P("This is the last step of our road. You should have"
                       " convinced yourself about which attribute should your"
                       " monsters and your deck have. The aim of this last graph"
                       "is the one of helping you to see which are the spell "
                       "and trap cards that are the most used within the decks that"
                       " have the attribute that you have choosen. If you are"
                       " concerned about the prices of the cards... don't worry "
                       "because the bars of each card are colored according to "
                       "their price in the cardmarket")
                ])
        ]))]),
    dbc.Row([
        dbc.Col([mytitle], width=6)
    ], justify='center'),
    dbc.Row([
        dbc.Col([mygraph], width=12)
    ]),
    dbc.Row([
        dbc.Col([html.Label('Spell or Trap'), radio_botton], width=6),
        dbc.Col([html.Label('Choose an Attribute'), dropdown], width=6)
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
    Input(radio_botton, 'value'),
    Input(dropdown, 'value')
)
def update_graph(frame, attribute):  # added price_range argument
    filtered_df2 = df_exploded.loc[df_exploded['frameType']==frame]     # filtering the df_exploded to have only rows with spell crads or trap cards
    filtered_df = df_exploded.loc[df_exploded['attribute']==attribute]  # filtering df_exploded according to the attribute chosen by the user

    # storing the names of the deck with the highest number of {attribute} card inside in a variable
    attribute_list=list(filtered_df['set_names'].value_counts().head(200).index.values)  # selecting the decks that have most cards of the attribute selected. Assigning the type to the decks

    # initializing the dictionary
    dict={}

    # loop through each row in the dataframe
    for index, row in filtered_df2.iterrows():
    # check if the set_name is in the list
        if row['set_names'] in attribute_list:
            if row['name'] in dict:
            # if so, increment the counter
                dict[row['name']] += 1
            else:
            # if not, add the name to the dictionary with a counter of 1
                dict[row['name']] = 1
        else:
        # if the set_name is not in the list, do nothing
            pass


    # Convert the dictionary to DataFrame
    df_counts = pd.DataFrame.from_dict(dict, orient='index', columns=['counting'])
    df_counts.index.name = 'card_name'
    df_counts.reset_index(inplace=True)
    # sorting the dataframe according to the counting variable
    df_counts=df_counts.sort_values(by='counting', ascending=False)
    df_price=df_exploded.groupby('name').agg({'cardmarket_price':'mean'})
    df_price['cardmarket_price']=df_price['cardmarket_price'].round(2)
    df_counts=pd.merge(df_counts, df_price, how='left', left_on='card_name', right_on='name')
    #plotting the graph
    fig=px.bar(df_counts.iloc[:14,], x='card_name', y='counting', hover_data=['cardmarket_price'],
               color='cardmarket_price', color_continuous_scale=scale)
    # setting the layout
    fig.update_layout(
    plot_bgcolor='#FFFFFF'
    )
    fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='LightGrey')
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='LightGrey')

    return fig














