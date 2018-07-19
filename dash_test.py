# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/' +
                 '5d1ea79569ed194d432e56108a04d188/raw/' +
                 'a9f9e8076b837d541398e999dcbac2b2826a81f8/' +
                 'gdp-life-exp-2007.csv')

axis_options = list(df.select_dtypes(include=['float64']).columns.values)

app = dash.Dash()

app.layout = html.Div(style={'backgroundColor': '#111111'}, children=[
    html.H1(children='Hello Dash',
            style={
                'fontFamily': 'Calibri',
                'textAlign': 'center',
                'color': '#cccccc'
            }),

    html.Div(children='''
        Dash: A web application framework for Python
    ''',
             style={
                 'fontFamily': 'Calibri',
                 'textAlign': 'center',
                 'color': '#cccccc'
             }),
    html.Div([
        dcc.Dropdown(
            id='y_axis',
            options=[{'label': item, 'value': item} for item in axis_options],
            value='population'
        )
    ],
        style={
            'width': '48%',
            'display': 'inline-block',
            'fontFamily': 'Calibri'
        }
    ),

    dcc.Graph(
        id='example-graph'
    ),

    dcc.Graph(
        id='pie',
        figure={
            'data': [
                go.Pie(
                    labels=df['continent'],
                    values=df['population'],
                    hole=0.5,
                    textfont={
                        'family': 'Calibri'
                    }
                )
            ],
            'layout': go.Layout(
                paper_bgcolor='#111111',
                plot_bgcolor='#111111'
            )
        }
    )
])


@app.callback(
    dash.dependencies.Output('example-graph', 'figure'),
    [dash.dependencies.Input('y_axis', 'value')])
def update_graph(y_axis_column_name):
    return {
        'data': [
            go.Scatter(
                x=df[df['continent'] == i]['gdp per capita'],
                y=df[df['continent'] == i][y_axis_column_name],
                text=df[df['continent'] == i]['country'],
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 15,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=i
            ) for i in df.continent.unique()
        ],
        'layout': go.Layout(
            xaxis={'title': 'GDP Per Capita'},
            yaxis={'type': 'log', 'title': y_axis_column_name},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            paper_bgcolor='#111111',
            plot_bgcolor='#111111'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
