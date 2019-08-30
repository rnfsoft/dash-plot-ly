import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.H4('Input Only'),
        dcc.Input(id='input-1', type='text', value='San Jose'),
        dcc.Input(id='input-2', type='text', value='San Francisco'),
        html.Div(id='number-output'),


        html.H4('State'),
        dcc.Input(id='input-1-state', type='text', value='San Jose'),
        dcc.Input(id='input-2-state', type='text', value='San Francisco'),
        html.Button(id='submit-button', n_clicks=0, children='Submit'),
        html.Div(id='output-state'),

        html.H4('PreventUpdate'),
        html.Button('Click here', id='button'),
        html.Div(id='body-div'),

        html.H4('No Update'),
        html.P('Enter a composite number to see its prime factors'),
        dcc.Input(id='num', type='number', min=1, step=1),
        html.P(id='err', style={'color': 'red'}),
    ]
)

@app.callback(
    Output('err', 'children'),
    [Input('num', 'value')]
)
def show_factors(num):
    if num is None:
        return PreventUpdate

    factors = prime_factors(num)
    if len(factors) == 1:

        return '{} is prime!'.format(num)

    return '{} is {}'.format(num, ' * '.join(str(n) for n in factors))


def prime_factors(num):
    n, i, out = num, 2, []
    while i * i <= n:
        if n % i == 0:
            n = int(n / i)
            out.append(i)
        else:
            i += 1 if i == 2 else 2
    out.append(n)
    return out

@app.callback(
    Output('body-div', 'children'),
    [Input('button', 'n_clicks')]
)
def update_output(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        return 'Elephants can jump'

@app.callback(
    Output('output-state', 'children'),
    [Input('submit-button', 'n_clicks')],
    [
        State('input-1-state', 'value'),
        State('input-2-state', 'value')
    ]
)
def update_output(n_clicks, input1, input2):
    return u'''
        The button has been pressed {} times,
        Input 1 is {}
        Input 2 is {}
    '''.format(n_clicks, input1, input2)

@app.callback(
    Output('number-output', 'children'),
    [Input('input-1', 'value'), Input('input-2', 'value')],
)
def update_output(input1, input2):
    return u'Input 1 is {} and Input 2 is {}'.format(input1, input2)






if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)