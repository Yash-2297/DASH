import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.graph_objects as go
import pandas as pd

df= pd.read_csv(r'C:\Users\yp229\Downloads\titanicdataset-traincsv\train.csv')
df_graph = df.groupby(['Embarked'])['PassengerId'].count().reset_index()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    
    html.Label('Select Gender'),
    dcc.Dropdown(
        id='Sex',
        options=[
            {'label': 'Male', 'value': 'male'},
            {'label':'Female','value':'female'},
          
        ],
    
    value = 'male'
        ,multi=False,
       
)
    # ),
    
    
    # html.Label('Select Age'),
    #     dcc.Dropdown(
    #     id='Age',
    #     options=[
    #         {'label':'<=18','value':'18'},
    #         {'label':'<=35','value':'35'},
    #         {'label':'<=50','value':'50'},
    #         {'label':'<=80','value':'80'},
    #         {'label':'<=100','value':'100'}
        
          
    #     ],
    #     value = '18',
    
    #     multi=False,
       

    # )
    #     ,
    #     html.Label('Select Class'),
    #     dcc.Dropdown(
    #     id='Pclass',
    #     options=[
    #         {'label': '1', 'value': '1'},
    #         {'label':'2','value':'2'},
    #         {'label':'3','value':'3'}
        
          
    #     ],
    
    #     multi=True,
       

    # ),
        
        
    #     html.Label('Select Cabin'),
    #     dcc.Dropdown(
    #     id='Cabin',
    #     options=[
    #         {'label': i, 'value': i}
            
    #         for i in df[df.Cabin.notnull()]['Cabin'].unique()
       
            
    #     ],
    
    #     multi=True,
       

    # )
    ,
    html.Div(
      id='cx1'
      ),
#         figure={
#             'data': [
#                 {'x': df_graph['Embarked'], 'y': df_graph['PassengerId'], 'type': 'bar', 'name': 'SF'}
      
#             ],
#             'layout': {
#                 'title': 'Dash Data Visualization'
#             }
#         }
        
# )
# ,


])

@app.callback(
    dash.dependencies.Output('cx1', 'children'),
    [dash.dependencies.Input('Sex', 'value')])
    
def update_figure(value):
    if value is None:
        graph = df
    else:
        graph = df[df['Sex'] == value].groupby(['Embarked'])['PassengerId'].count().reset_index()

    return html.Div(
            dcc.Graph(
                id='bar chart',
                figure={
                    "data": [
                        {
                            "x": graph['Embarked']
                            ,"y": graph['PassengerId']
                            ,"type": "bar",
                            "marker": {"color": "#0074D9"},
                            "text" : "y"
                        }
                    ],
                    "layout": {
                        'title': 'Basic Dash Bar',
                        "xaxis": {"title": "Embarked"},
                        "yaxis": {"title": "Counts"},
                        # 'plot_bgcolor': colors['background'],
                        # 'paper_bgcolor': colors['background']
                    },
                },
            )
    )



if __name__ == '__main__':
    app.run_server(debug=False)
       
    ;
                

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
])


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            filter_action = "native",
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])


@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children



if __name__ == '__main__':
    app.run_server(debug=False)