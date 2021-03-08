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

    ])


@app.callback(
    [
        Output(component_id='my-title', component_property='children'),
        Output(component_id='my-plot', component_property='figure')
    ],
    [
        Input(component_id='my-input', component_property='value'),
        Input(component_id='min-price', component_property='value'),
        Input(component_id='max-price', component_property='value')
    ]
)
def update_plot(url, min, maxi):
    title, fig = data.plot_serials(url, min, maxi)
    return title, fig


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)