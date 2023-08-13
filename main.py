import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
from dash import dash_table

# Load the data from the Excel files
df = pd.read_excel("combined_esg_data.xlsx", sheet_name="ESG Data")
profile_df = pd.read_excel("combined_esg_data.xlsx", sheet_name="Company Profiles")
financials_df = pd.read_excel("combined_esg_data.xlsx", sheet_name="Financials")
reply = str('test output')

# Initialize the Dash app
app = dash.Dash(__name__)

# Create a list of unique company names
all_companies = profile_df['longName'].unique()

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Company analytics dashboard for portfolio managers"),
    
    html.H2("1. Filter"),
    html.Div([
        dcc.Dropdown(
            id='company-dropdown',
            options=[
                {'label': 'All Companies', 'value': 'All Companies'}
            ] + [{'label': company, 'value': company} for company in all_companies],
            multi=True,
            value=['All Companies']  # Initial value
        ),
    ], style={'width': '25%', 'display': 'inline-block'}),
    html.Br(),  # Add a line break
    
    html.Div([
        dcc.Dropdown(
            id='score-dropdown',
            options=[
                {'label': 'ESG Score', 'value': 'esgScore'},
                {'label': 'Governance Score', 'value': 'governanceScore'},
                {'label': 'Environment Score', 'value': 'environmentScore'},
                {'label': 'Social Score', 'value': 'socialScore'}
            ],
            multi=True,
            value=['esgScore']  # Initial value
        ),
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date='2020-01-01',
            end_date=df['timestamp'].max(),
            display_format='YYYY-MM-DD'
        ),
    ], style={'width': '25%', 'display': 'inline-block'}),
    html.Br(),  # Add a line break
    
    html.H2("2. ESG Scores Over Time"),
    dcc.Graph(id='esg-graph'),
    
    html.H2("3. Company Profiles"),
    html.Div(id='company-tiles', style={'display': 'flex', 'flex-wrap': 'wrap', 'max-width': '100%'}),

    html.H2("4. Financials"),
    dcc.Loading(
        id="loading-table",
        type="circle",
        children=[
            dash_table.DataTable(
                id='financials-table',
                columns=[
                    {'name': 'Company Name', 'id': 'Company name'},
                    {'name': 'As of Date', 'id': 'asOfDate'},
                    {'name': 'Total Revenue', 'id': 'TotalRevenue'},
                ],
                style_table={'width': '100%'},
                style_data={'whiteSpace': 'normal', 'height': 'auto'},
                sort_action="native",
                sort_mode="multi",
                filter_action="native",
            )
        ],
    ),
    html.H2("5. ChatGPT opinion"),
    dcc.Textarea(
        id='chatgpt-opinion',
        value=reply,
        rows=30,
        style={'width': '100%'}
    ),
])

# Callback to update the graph and company tiles
@app.callback(
    [Output('esg-graph', 'figure'), Output('company-tiles', 'children')],
    [Input('company-dropdown', 'value'),
     Input('score-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_graph(selected_companies, selected_scores, start_date, end_date):
    if 'All Companies' in selected_companies:
        selected_companies = all_companies

    filtered_df = df[df['longName'].isin(selected_companies)]
    filtered_df = filtered_df[(filtered_df['timestamp'] >= start_date) & (filtered_df['timestamp'] <= end_date)]

    fig = px.line(
        filtered_df,
        x='timestamp',
        y=selected_scores,
        color='longName',
        labels={'timestamp': 'Date', 'value': 'Score'},
    )

    company_tiles = []
    for company_name in selected_companies:
        profile = profile_df[profile_df['longName'] == company_name].iloc[0]
        tile = html.Div([
            html.H3(profile['longName']),
            html.P(profile['longBusinessSummary'], id=f'summary-{company_name}', style={'max-height': '100px', 'overflow': 'hidden', 'padding-bottom': '10px'}),  # Adjust padding here
            html.Button('Read More', id=f'button-{company_name}', n_clicks=0),
            html.Div([], id=f'remainder-{company_name}', style={'max-height': '1000px', 'overflow': 'hidden'}),
        ], style={'width': '28%', 'margin': '10px', 'border': '1px solid gray', 'padding': '30px'})
        company_tiles.append(tile)

    return fig, company_tiles

# Callback for toggling show more/show less dynamically
@app.callback(
    [Output('summary-All Companies', 'style'),
     Output('remainder-All Companies', 'style'),
     Output('button-All Companies', 'children')],
    [Input('button-All Companies', 'n_clicks')],
    [State('summary-All Companies', 'style'),
     State('remainder-All Companies', 'style'),
     State('button-All Companies', 'children')]
)
def toggle_text(n_clicks, current_summary_style, current_remainder_style, button_text):
    if n_clicks % 2 == 0:
        return {'max-height': '100px', 'overflow': 'hidden'}, {'max-height': '1000px', 'overflow': 'hidden'}, 'Read More'
    else:
        return {'max-height': '1000px', 'overflow': 'hidden'}, {'max-height': '1000px', 'overflow': 'hidden'}, 'Show Less'

# Callbacks for toggling show more/show less for each company
for company_name in all_companies:
    @app.callback(
        [Output(f'summary-{company_name}', 'style'),
         Output(f'remainder-{company_name}', 'style'),
         Output(f'button-{company_name}', 'children')],
        [Input(f'button-{company_name}', 'n_clicks')],
        [State(f'summary-{company_name}', 'style'),
         State(f'remainder-{company_name}', 'style'),
         State(f'button-{company_name}', 'children')]
    )
    def toggle_text(n_clicks, current_summary_style, current_remainder_style, button_text, company=company_name):
        if n_clicks % 2 == 0:
            return {'max-height': '100px', 'overflow': 'hidden'}, {'max-height': '1000px', 'overflow': 'hidden'}, 'Read More'
        else:
            return {'max-height': '1000px', 'overflow': 'hidden'}, {'max-height': '1000px', 'overflow': 'hidden'}, 'Show Less'

# Callback to update financials table
@app.callback(
    Output('financials-table', 'data'),
    [Input('company-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_financials_table(selected_companies, start_date, end_date):
    if 'All Companies' in selected_companies:
        selected_companies = all_companies

    filtered_financials = financials_df[financials_df['Company name'].isin(selected_companies)]
    filtered_financials = filtered_financials[(filtered_financials['asOfDate'] >= start_date) & (filtered_financials['asOfDate'] <= end_date)]

    return filtered_financials.to_dict('records')
