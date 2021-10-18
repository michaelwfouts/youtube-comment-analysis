import pandas as pd
import plotly.express as px

import dash
from dash import dcc # dash core components
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

#---------
# import and clean data (importing csv into pandas)
df = pd.read_csv("fullCommentDatasetWithSentiment.csv")
dff = df.copy()
dff = dff.groupby(['uploadTime','title']).comments.count().reset_index()
dff['uploadTime'] = pd.to_datetime(dff['uploadTime'])
ax = px.scatter(data_frame=dff,
                        x = 'uploadTime',
                        y = 'comments',
                        hover_name='title',
                        opacity = 0.6)

ax.update_layout(
    title = 'Video Upload Date vs. Number of Parent Comments Posted',
    xaxis_title = 'Video Upload Date',
    yaxis_title = 'Number of Comments Posted'
)

ax.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)',
'font_color': 'white'
})

ax2 = px.histogram(data_frame = df,
                   x = 'compound_sentiment',
                   nbins = 11)

ax2.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)',
'font_color': 'white'
})

ax2.update_layout(
    title = 'Distribution of Parent Comment Sentiments Across All Videos',
    xaxis_title = 'Compound Sentiment',
    yaxis_title = 'Number of Parent Comments'
)


# define main components of the dashboard

# Channel Metrics
channelMetricGraphs = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card(
                # graph output
                dcc.Graph(figure = ax),
                color = 'black'
            ),
        ])
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Card(
                # graph output
                dcc.Graph(figure = ax2),
                color = 'black'
            ),
        ])
    ])
])


# video filter
videoFilter = dbc.Row([
    dbc.Col([
        html.Label('Select Video'),
        dbc.Select(
            id = 'videoFilter',
            options=[
                {'label':i, 'value':i} for i in df['title'].unique()
            ],
            value = df['title'][0],
            style = {
                'background-color': 'rgb(48, 48, 48)',
                'color': 'white',
                'border': '2px solid white',
            },
        )
    ])
])

# Filter criteria bar for single video comments
commentsFilter = dbc.Row([
        dbc.Col([
            html.Label('Number of Comments to Analyze'),
            html.Br(),
            dbc.Input(
                id = 'comment_num',
                placeholder = 'Please Enter a Value',
                type = 'number',
                value = 2,
                style={ # this is css code
                    'background-color': 'rgba(0, 0, 0, 0)',
                    'color': 'white',
                    'border': '2px solid white'
                }
            ),
        ], width={'size':4}),
        dbc.Col([
            html.Label('Minimum Number of Likes'),
            html.Br(),
            dbc.Input(
                id = 'likes_min',
                placeholder = 'Please Enter a Value',
                type = 'number',
                value = 0,
                style={ # this is css code
                    'background-color': 'rgba(0, 0, 0, 0)',
                    'color': 'white',
                    'border': '2px solid white'
                }
            ),
        ], width={'size':4}),
        dbc.Col([
            html.Label('Minimum Number of Replies'),
            html.Br(),
            dbc.Input(
                id = 'replies_min',
                placeholder = 'Please Enter a Value',
                type = 'number',
                value = 0,
                style={ # this is css code
                    'background-color': 'rgba(0, 0, 0, 0)',
                    'color': 'white',
                    'border': '2px solid white'
                }
            ),
        ], width={'size':4})
    ])

# graph layout for a single video comment analysis
videoCommentGraphs = dcc.Tabs([
                        dcc.Tab(label='Graph',
                        style={
                            'background-color': 'rgba(0, 0, 0, 0)',
                            'color': 'white', # text color
                        },
                        selected_style={
                            'background-color': 'black',
                            'color': 'white'
                        },
                        children=[
                            html.Br(),
                            # Compound Hist
                            dbc.Row([
                                dbc.Col([
                                    dbc.Card(
                                        # graph output
                                        dcc.Graph(id = 'compound_hist', figure={}),
                                        color = 'black'
                                    )
                                ], width={'size':12})
                            ]),

                            html.Br(),

                            # Scatter plot
                            dbc.Row([
                                dbc.Col([
                                    dbc.Card(
                                        # graph output
                                        dcc.Graph(id = 'comment_scatter', figure={}),
                                        color = 'black'
                                    )
                                ], width={'size':12})
                            ]),

                            html.Br(),

                            dbc.Row([
                                dbc.Col([
                                    dbc.Card(
                                        # graph output
                                        dcc.Graph(id = 'negative_hist', figure={}),
                                        color = 'black'
                                    ),  
                                ], width={'size':4}),
                                dbc.Col([
                                    dbc.Card(
                                        # graph output
                                        dcc.Graph(id = 'neutral_hist', figure={}),  
                                        color = 'black'
                                    ),
                                ], width={'size':4}),
                                dbc.Col([
                                    dbc.Card(
                                        # graph output
                                        dcc.Graph(id = 'positive_hist', figure={}),  
                                        color = 'black'
                                    ),
                                ], width={'size':4})
                            ]),         
                                            
                        ]),

                        dcc.Tab(label='Table',
                        style={
                            'background-color': 'rgba(0, 0, 0, 0)',
                            'color': 'white'
                        },
                        selected_style={
                            'background-color': 'black',
                            'color': 'white'
                        },
                        children=[
                            html.Br(),
                            # download button
                            html.Div([
                                    dbc.Button("Downlad CSV", color = 'light', id = "btn_csv", className = 'mr-1'),
                                    dcc.Download(id="download-data-csv")                    
                                    ]),
                            html.Br(),
                            # this gives a table output in the below callback
                            html.Div([
                            html.Div(id = 'div-1'),
                            ])
                        ]),
                    ])

#---------
channelMetricsTab = dbc.Card(
    dbc.CardBody(
        [
            channelMetricGraphs            
        ]
    ),
    className="mt-3",
)

videoSentimentTab = dbc.Card(
    dbc.CardBody(
        [
            videoFilter,
            commentsFilter,
            html.Br(),
            videoCommentGraphs,
        ]
    ),
    className="mt-3",
)

additionalIndo = dbc.Card(
    dbc.CardBody(
        [
            html.H1('Purpose', className = "card-text"),
            html.P("The purpose of this dashboard is to give a visual representation of the metrics evaluated in my end to end personal project of evaluating YouTube Comments.  Other portions include using the YouTube API to gather the data, uploading to Google BigQuery, and performing some Natural Language Processing."),
            html.H2('Contact Info'),
            html.B("Email:"),
            html.P("michaelwfouts@gmail.com", className="card-text"),
            html.Br(),
            html.B("GitHub:"),
            html.P("https://github.com/michaelwfouts", className="card-text"),
        ]
    ),
    className="mt-3",
)

mainTabs = dbc.Tabs(
        [
            dbc.Tab(channelMetricsTab, label = "Channel Metrics"),
            dbc.Tab(videoSentimentTab, label = "Video Sentiment"),
            dbc.Tab(additionalIndo, label = "Additional Info")
        ]
    )

# app layout.  This is where the graph components (inputs) go and is the front end
app.layout = dbc.Container([
    html.H1("YouTube Comment Section Analysis", style = {'text-align': 'left'}),

    mainTabs,
    
    html.Br(),

    

])

#------------
# call back (server portion of the function)
@app.callback(
    Output('div-1','children'),
    Output(component_id='positive_hist', component_property='figure'),
    Output(component_id='negative_hist', component_property='figure'),
    Output(component_id='comment_scatter', component_property='figure'),
    Output(component_id='compound_hist', component_property='figure'),
    Output(component_id='neutral_hist', component_property='figure'),
    Input('comment_num','value'),
    Input('likes_min', 'value'),
    Input('replies_min', 'value'),
    Input('videoFilter', 'value')
)

# each argument in the function under the callback relates to an input above
def callback_a(x, min_likes, min_replies, videoFilter):
    
    dff = df.copy()
    dff = dff.drop(['commentsId','videoId','channelId','no_stop'], axis = 1)
    dff = dff[(dff['title'] == videoFilter)]
    dff = dff[(dff['likesCount'] >= min_likes) & (dff['repliesCount'] >= min_replies)]
    dff = dff[:x]

    # histogram of positive sentiment
    fig_pos = px.histogram(dff, x='pos_sentiment')

    fig_pos.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    'font_color': 'white'
    })

    fig_pos.update_layout(
    title = 'Positive Sentiment Histogram',
    xaxis_title = 'Positive Sentiment Intensity',
    yaxis_title = 'Number of Parent Comments'
    )

    # histogram of negative sentiment
    fig_neg = px.histogram(dff, x='neg_sentiment')

    fig_neg.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    'font_color': 'white'
    })

    fig_neg.update_layout(
    title = 'Negative Sentiment Histogram',
    xaxis_title = 'Negative Sentiment Intensity',
    yaxis_title = 'Number of Parent Comments'
    )

    fig_neu = px.histogram(dff, x='neu_sentiment')

    fig_neu.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    'font_color': 'white'
    })

    fig_neu.update_layout(
    title = 'Neutral Sentiment Histogram',
    xaxis_title = 'Neutral Sentiment Intensity',
    yaxis_title = 'Number of Parent Comments'
    )

    # comment scatterplot
    comment_scatterplot = px.scatter(dff, 
                                     x = 'compound_sentiment', 
                                     y = 'likesCount', 
                                     hover_name='comments',
                                     custom_data = ['repliesCount', 'comments'],
                                     opacity=0.7,
                                     )

    comment_scatterplot.update_traces(hovertemplate='<b>%{customdata[1]}</b><br> <br>Likes: %{y} <br>Replies: %{customdata[0]}')

    comment_scatterplot.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    'font_color': 'white'
    })
    
    comment_scatterplot.update_layout(
    title = 'Video Comment Sentiment vs Number of Likes',
    xaxis_title = 'Compound Sentiment',
    yaxis_title = 'Number of Likes'
    )

    comment_scatterplot.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')),
                  selector=dict(mode='markers'))

    fig_compound = px.histogram(dff, x='compound_sentiment')

    fig_compound.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    'font_color': 'white'
    })

    fig_compound.update_layout(
    title = 'Video Sentiment Histogram',
    xaxis_title = 'Compound Sentiment',
    yaxis_title = 'Number of Parent Comments'
    )

    # the return is the outputs above
    return [
        dash_table.DataTable(
            id = 'table',
            columns = [{"name": i, "id": i} for i in dff.columns],
            data = dff.to_dict('records'),
            filter_action="native",
            sort_action="native",
            style_header={
            'backgroundColor': 'black',
            'fontWeight': 'bold'
            },
            style_filter={
            'backgroundColor': 'black',
            },
            style_data={
            'backgroundColor': 'transparent'
            },
            css= [{'selector': 'tr:hover', 'rule': 'background-color: gray;'}],
            style_cell={
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'maxWidth': 0
            },
        ),
        # return figures
        fig_pos, fig_neg, comment_scatterplot, fig_compound, fig_neu

    ]

@app.callback(
    Output("download-data-csv","data"),
    Input('btn_csv','n_clicks'),
    State('comment_num','value'),
    State('likes_min', 'value'),
    State('replies_min', 'value'),
    State('videoFilter', 'value')
)

def callback_b(n_clicks, x, min_likes, min_replies, videoFilter):
        
        dff = df.copy()
        dff = dff[(dff['title'] == videoFilter)]
        dff = dff[(dff['likesCount'] >= min_likes) & (dff['repliesCount'] >= min_replies)]
        dff = dff[:x]
        
        # return downloadable dataframe
        return dcc.send_data_frame(dff.to_csv, "mydf.csv")

#---------------
# run the app

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True)