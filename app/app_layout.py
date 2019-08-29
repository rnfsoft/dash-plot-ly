import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

# import numpy as np
# from datetime import datetime, timedelta
# import plotly.graph_objs as go

# date_today = datetime.now()
# days = pd.date_range(date_today, date_today+timedelta(30), freq='D')
# sales = np.random.randint(70, high=100, size=len(days))
# data = pd.DataFrame({'date': days, 'Sales': sales})


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df1 = pd.read_csv('https://gist.githubusercontent.com/chriddyp/'
    'c78bf172206ce24f77d6363a2d754b59/raw/'
    'c353e8ef842413cae56ae3920b8fd78468aa4cb2/'
    'usa-agricultural-exports-2011.csv')

'''
    --origin data--
    ,state,total exports,beef,pork,poultry,dairy,fruits fresh,fruits proc,total fruits,veggies fresh,veggies proc,total veggies,corn,wheat,cotton
    0,Alabama,1390.63,34.4,10.6,481.0,4.06,8.0,17.1,25.11,5.5,8.9,14.33,34.9,70.0,317.61
    1,Alaska,13.31,0.2,0.1,0.0,0.19,0.0,0.0,0.0,0.6,1.0,1.56,0.0,0.0,0.0
'''

df2 = pd.read_csv('https://gist.githubusercontent.com/chriddyp/' +
    '5d1ea79569ed194d432e56108a04d188/raw/' +
    'a9f9e8076b837d541398e999dcbac2b2826a81f8/'+
    'gdp-life-exp-2007.csv')

'''
    --origin data--
    ,country,continent,population,life expectancy,gdp per capita
    11,Afghanistan,Asia,31889923.0,43.828,974.5803384
    23,Albania,Europe,3600523.0,76.423,5937.029526
    35,Algeria,Africa,33333216.0,72.301,6223.367465
'''
def generate_table(dataframe, max_rows=10):
    return html.Table(
        [html.Tr([html.Th(col) for col in dataframe.columns])] +
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

markdown_text = '''
### Dash and Markdown

Dash apps can be written in Markdown.
Dash uses the [CommonMark](http://commonmark.org/)
specification of Markdown.
Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)
if this is your first introduction to Markdown!
'''

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div([
    html.H1('Hello Dash'),

    html.Div('''
        Dash: A web application framework for Python
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data':[
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'SJ'},
            ],
            'layout': {
                'title': 'Dash Data Visulization'
            }
        }
    ),
    
    html.H4('CSV example'),
    generate_table(df1),

    html.H4('Graph example'),
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure={
            'data': [
                go.Scatter(
                    x=df2[df2['continent'] == i]['gdp per capita'],
                    y=df2[df2['continent'] == i]['life expectancy'],
                    text=df2[df2['continent'] == i]['country'], # when hover on dot
                    mode='markers',
                    opacity=0.7, # dot darkness
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'} # edge
                    },
                    name= i
                ) for i in df2.continent.unique()
            ],
            'layout': go.Layout(
                xaxis={'type': 'log', 'title': 'GDP Per Capita'},
                yaxis={'title': 'Life Expectancy'},
                margin={'l':40, 'b':40, 't':50, 'r':10},
                legend={'x': 0, 'y':1},
                hovermode='closest'
            )
        }
    ),

    html.H4('Markdown example'),
    dcc.Markdown(markdown_text),

    html.H4('Components examples'),
    html.Label('Dropdown'),
    dcc.Dropdown(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='SF'
    ),

    html.Label('Multi-Selection'),
    dcc.Dropdown(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value=['NYC', 'SF'],
        multi = True
    ),

    html.Label('Radio Items'),
    dcc.RadioItems(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='SF'
    ),

    html.Label('Checkboxes'),
    dcc.Checklist(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value=['NYC', 'SF'],
    ),

    html.Label('Text Input'),
    dcc.Input(value='SF', type='text'),

    html.Label('Slider'),
    dcc.Slider(
        min = 0,
        max = 9,
        marks = {i: 'Label {}'.format(i) if i == 1 else str(i) for i in range(1, 6)},
        value=5,
    )


    
])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0',debug=True)