import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

colors = {
    'background': '#111111',
    'text': '#4264ed'
}

df = pd.DataFrame(data={'a': [2, 4], 'b': [4, 8]})
fig = px.bar(df)
fig.update_layout(
    font_color=colors['text']
)

app.layout = html.Div(
    # style={'backgroundColor': colors['background']},
    children=[
        html.H1(children='Hello Top Shot', style={'textAlign': 'center', 'color': colors['text']}),
        dcc.Graph(id='my-plot', figure=fig),
        dcc.Input(id='my-input', placeholder="text here", type='text'),
        html.Br(),
        html.Div(id='my-output')
    ])


@app.callback(
    Output(component_id='my-plot', component_property='figure'),
    Input(component_id='my-input', component_property='value')
)
def update_plot(input_val):
    df.a = df.a + 1
    df.b = df.b - 1
    return px.bar(df)


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)