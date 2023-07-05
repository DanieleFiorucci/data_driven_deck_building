#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dash_html_components as html
import dash

# connecting the page to the app.py file
dash.register_page(__name__, path='/page-5', name='Contact us')

# Customize your own Layout
layout = html.Div([
    html.H1('Contact us'),
    html.Div([
        html.P("Our road ends here. We hope this web site could have helped you"
               " in constructing the best possible deck. Hope that you will win"
               " a lot of games with your brand new deck. Don't esitate to tell"
               " to your friends about us and if you need some suggestions about"
               " the Yu-Gi-Oh game contact us, we will be glad to help you."
               " Hope to see you soon!!!")
        ])
])

