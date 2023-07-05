#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# DASH 1 -Scatter Plot
import dash_html_components as html
import dash
#from PIL import Image
import dash_bootstrap_components as dbc

# connecting the page to the app.py file
dash.register_page(__name__, path='/', name='Home')

# # setting the features for the image that we want on pour page
# image_path = Image.open('pages/logo.png')
# new_width = 726
# new_height = 256
# resized_image = image_path.resize((new_width, new_height))


# Customize your own Layout
layout = html.Div([
#    html.H1('Welcome to out web site'),
    dbc.Row([
        dbc.Col([
            html.Div(style={'height': '25px'})
            ])
        ], justify='center'),
    html.Div([
 #       html.Img(src=resized_image), 
        dbc.Row([
            dbc.Col([
                html.Div(style={'height': '50px'})
                ])
            ], justify='center'),
        html.P('Hi, we are three students attending the Data Visualization course,'
               'we are old fans of the yu-gi-oh game. With this web site we would' 
               'like to help new players that like this game (as we did) to build the deck they'
               ' most prefered based on the data we have gathered. What the user of'
               ' this page will find will be some static graphs show ingthe type of data'
               ' that have been used adn then some interactive graphs that will be useful in the construction of the deck.')
        ]),
    html.Div([
        html.H3('Our Data'),
        html.P('In order to build this web site we retrieved our data from an'
               ' API about Yu-Gi-Oh cards. Inside that dataset there were quite'
               ' a lot of data and after have cleaned them a bit we decided to'
               ' construct a datset with the most usefull data to solve '
               'our task. Therefore, the data we will be using all along the '
               'journey in the site are data about the card name, their type,'
               ' the attribute of the monster cards, their attack , defense and'
               ' level, the price of the cards and the names of the sets in '
               'which they are used and the rarity of the sets')
        ]),
    dbc.Row([
        dbc.Col([
            html.Div(style={'height': '50px'})
            ])
        ], justify='center')
])
