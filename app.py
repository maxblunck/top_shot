import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import data

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

colors = {
    'background': '#111111',
    'text': '#4264ed'
}
default = "https://www.nbatopshot.com/listings/p2p/12a8288a-addc-4e5c-8af7-b3ba6e5161d4+9c0cd57c-8203-4ec1-9a0c-9b7e7a6f0635"
title, fig = data.plot_serials(url=default)
fig.update_layout(
    font_color=colors['text']
)

app.layout = html.Div(
    # style={'backgroundColor': colors['background']},
    children=[
        html.H1(children='Top Shot Hot Stats', style={'textAlign': 'center', 'color': colors['text']}),
        html.H2("Bogdan", id='my-title', style={'fontSize': 20, 'textAlign': 'left', 'color': 'black'}),
        dcc.Graph(id='my-plot', figure=fig),
        dcc.Input(id='my-input', placeholder="Paste Top Shot Moment URL here...", type='text', size='120'),
        html.Br(),
        dcc.Input(id='min-price', placeholder="min price", type='text', size='20'),
        dcc.Input(id='max-price', placeholder="max price", type='text', size='20'),
        html.Button('Reset', id='reset-price'),
        html.Br(),
        dcc.Input(id='min-ser', placeholder="lowest serial", type='text', size='20'),
        dcc.Input(id='max-ser', placeholder="highest serial", type='text', size='20'),
        html.Button('Reset', id='reset-ser'),
        html.Br(),
        dcc.Dropdown(
            id='reduce-option',
            options=[
                {'label': 'All Serials', 'value': 'all'},
                {'label': 'Lowest Serial per Price', 'value': 'lowest'}
            ],
            value='all',
            style={"width": "50%"},
        )
    ])


@app.callback(
    [
        Output(component_id='my-title', component_property='children'),
        Output(component_id='my-plot', component_property='figure')
    ],
    [
        Input(component_id='my-input', component_property='value'),
        Input(component_id='min-price', component_property='value'),
        Input(component_id='max-price', component_property='value'),
        Input(component_id='min-ser', component_property='value'),
        Input(component_id='max-ser', component_property='value'),
        Input(component_id='reduce-option', component_property='value'),
    ]
)
def update_plot(url, min_price, max_price, min_ser, max_ser, reduce):
    title, fig = data.plot_serials(url, reduce, min_price, max_price, min_ser, max_ser)
    return title, fig


@app.callback(
    Output(component_id='min-price', component_property='value'),
    Output(component_id='max-price', component_property='value'),
    Input(component_id='reset-price', component_property='n_clicks')
)
def reset_price(value):
    return None, None


@app.callback(
    Output(component_id='min-ser', component_property='value'),
    Output(component_id='max-ser', component_property='value'),
    Input(component_id='reset-ser', component_property='n_clicks')
)
def reset_ser(value):
    return None, None


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)