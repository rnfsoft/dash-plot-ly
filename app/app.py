import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go
import random

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
'''
    origin data
    ountry,year,pop,continent,lifeExp,gdpPercap
    Albania,1952,1282697,Europe,55.23,1601.056136
    Albania,1957,1476505,Europe,59.28,1942.284244
    Albania,1962,1728137,Europe,64.82,2312.888958

'''

df2 = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/cb5392c35661370d95f300086accea51/raw/8e0768211f6b747c0db42a9ce9a0937dafcbd8b2/indicators.csv'
)
'''
,Country Name,Indicator Name,Year,Value
0,Arab World,"Agriculture, value added (% of GDP)",1952,
1,Arab World,CO2 emissions (metric tons per capita),1952,
2,Arab World,Domestic credit provided by financial sector (% of GDP),1952,
3,Arab World,Electric power consumption (kWh per capita),1952,
4,Arab World,Energy use (kg of oil equivalent per capita),1952,
5,Arab World,Exports of goods and services (% of GDP),1952,
'''
df2['Value'] = df2['Value'].apply(lambda x: random.random() * 100 ) 
# pd.set_option('display.expand_frame_repr', False)
# print(df2.head())
available_indicators = df2['Indicator Name'].unique()

all_optioins = {
    'America': ['New York', 'San Francisco', 'Chicago'],
    'Korea': ['Seoul', 'Busan']
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

app.layout = html.Div([
    dcc.Input(id='my-id', value='initial value', type='text'),
    html.Div(id='my-div'),

    html.H4('Graph with Slider example'),
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        step= None
    ),
    
    html.Hr(),
    html.H4('Multiple Inputs'),
    html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value':i} for i in available_indicators],
                value='Fertility rate, total (births per woman)'
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label':i, 'value':i} for i in ['Linear', 'Log']],
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value':i} for i in available_indicators],
                value='Life expectancy at birth, total (years)'
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label':i, 'value':i} for i in ['Linear', 'Log']],
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        dcc.Graph(id='indicator-graphic'),

        dcc.Slider(
        id='year--slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        step= None
    ),

    html.Hr(),
    html.H4('Multiple Outputs'),
    dcc.Input(
        id='num',
        type='number',
        value=5
    ),
    html.Table([
        html.Tr([html.Td(['x', html.Sup(2)]),html.Td(id='square')]),
        html.Tr([html.Td(['x', html.Sup(3)]),html.Td(id='cube')]),
        html.Tr([html.Td([2, html.Sup('x')]),html.Td(id='twos')]),
        html.Tr([html.Td([3, html.Sup('x')]),html.Td(id='threes')]),
        html.Tr([html.Td(['x', html.Sup('x')]),html.Td(id='x^x')]),
        
    ]),
    html.Hr(),
    html.H4('Chained Callbacks'),
    html.Div(
        [dcc.RadioItems(
            id='countries-dropdown',
            options=[{'label':k, 'value': k} for k in all_optioins.keys()],
            value='America'
        )],
        style={'width': '48%', 'display': 'inline-block'}),
    html.Div(
        [dcc.RadioItems(id='cities-dropdown')],
        style={'width': '48%', 'display': 'inline-block'}),
    html.Div(id='display-selected-values')


])

@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)
def update_output_div(input_value):
    return 'You\'ve entered {}'.format(input_value)

@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]
    traces = []
    for i in filtered_df.continent.unique():
        df_by_continent = filtered_df[filtered_df['continent'] == i]
        traces.append(go.Scatter(
            x=df_by_continent['gdpPercap'],
            y=df_by_continent['lifeExp'],
            text=df_by_continent['country'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width':0.5, 'color': 'white'}
            },
            name=i
        ))
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type':'log', 'title': 'GDP Per Capita'},
            yaxis={'title': 'Life Expectancy', 'range':[20, 90]},
            margin={'l':40, 'b':40, 't':10, 'r':10},
            hovermode='closest'
        )
    }

#### Multiple Inputs
@app.callback(
    Output('indicator-graphic', 'figure'),
    [
        Input('xaxis-column', 'value'),
        Input('yaxis-column', 'value'),
        Input('xaxis-type', 'value'),
        Input('yaxis-type', 'value'),
        Input('year--slider', 'value')

    ])
def update_graph(xaxis_column_name, yaxis_column_name, xaxis_type, yaxis_type, year_value):
    dff = df2[df2['Year'] == year_value]
 
    return {
        'data': [go.Scatter(
            x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

#### Multiple Outputs
@app.callback(
    [
        Output('square', 'children'),
        Output('cube', 'children'),
        Output('twos', 'children'),
        Output('threes', 'children'),
        Output('x^x', 'children')
    ],
    [Input('num', 'value')]
)
def callback_a(x):
    return x**2, x**3, 2**x, 3**x, x**x


#### Chained Callback
@app.callback(
    Output('cities-dropdown', 'options'),
    [Input('countries-dropdown', 'value')])
def set_cities_options(selected_country):
    return [{'label':i, 'value':i} for i in all_optioins[selected_country]]

@app.callback(
    Output('cities-dropdown', 'value'),
    [Input('cities-dropdown', 'options')])
def set_cities_values(avaiable_options):
    return avaiable_options[0]['value'] # it sets it to the first value in that options array.

@app.callback(
    Output('display-selected-values', 'children'),
    [
        Input('countries-dropdown', 'value'),
        Input('cities-dropdown', 'value')])
def set_display_children(selected_country, selected_city):
    return u'{} is a city in {}'.format(
        selected_city, selected_country,
    )

if __name__=='__main__':
    app.run_server(host='0.0.0.0', debug=True)