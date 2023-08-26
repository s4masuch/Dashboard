import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
from dash import dash_table
from dash import dcc, html, Input, Output, State
import base64
import dash_html_components as html
import os

# Custom functions from my modules
from upload_ISINs import upload_isins_to_github
from create_data_frames import create_data_frames
from enhancing_with_GPT import enhance_data


# Load the data from the Excel files
df = pd.read_excel("Data/Data_Frames/combined_esg_data.xlsx", sheet_name="ESG Data")
profile_df = pd.read_excel("Data/Data_Frames/combined_esg_data.xlsx", sheet_name="Company Profiles")
financials_df = pd.read_excel("Data/Data_Frames/combined_esg_data.xlsx", sheet_name="Financials")

# Path to the directory for ISIN uploads
isin_upload_dir = "Data/ISIN-Upload/"

# Initialize the Dash app
app = dash.Dash(__name__)

repo_owner = os.environ.get("REPO_OWNER")
repo_name = os.environ.get("REPO_NAME")

# Create a server variable that points to the underlying Flask server
server = app.server

# Create a list of unique company names
all_companies = profile_df['longName'].unique()

# Get ChatGPT message
excel_filename = 'Data/Data_Frames/latest_financials.xlsx'
enhanced_reply = enhance_data(excel_filename)
chatgpt_message = f"ChatGPT: {enhanced_reply}"




# Define the style for the whole dashboard
dashboard_style = {
    'font-family': 'verlag'
}


# Define the layout of the dashboard
app.layout = html.Div(style=dashboard_style, children=[
    html.Div(
        html.H1("Julius Bär Portfolio Management Dashboard", style={'color': 'white', 'background-color': 'rgb(20, 30, 85)', 'padding': '10px'}),
        style={'text-align': 'center'}
    ),
    html.H2("Upload ISINs"),
    dcc.Upload(
        id='upload-data',
        children=html.Button('Upload ISINs'),
        multiple=False
    ),
    html.Div(id='isin-status', style={'margin-top': '10px'}),
    html.Div(id='confirmation-message', style={'margin-top': '10px'}),

    html.H2("Data Enhancing"),
    html.Button('Data Enhancing', id='data-enhancing-button'),
    dcc.Loading(
        id="loading-enhancing",
        type="circle",
        children=[html.Div(id='confirmation-message', style={'margin-top': '10px'})],
    ),

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
    
    html.H2("ESG Scores Over Time"),
    dcc.Graph(id='esg-graph'),
    
    html.H2("Company Profiles"),
    html.Div(id='company-tiles', style={'display': 'flex', 'flex-wrap': 'wrap', 'max-width': '100%'}),

    html.H2("Financials"),
    dcc.Loading(
        id="loading-table",
        type="circle",
        children=[
            dash_table.DataTable(
                id='financials-table',
                columns=[
                    {'name': 'Company Name', 'id': 'Company name'},
                    {'name': 'As of Date', 'id': 'asOfDate'},
                    {'name': 'Basic Average Share', 'id': 'BasicAverageShares'},
                    {'name': 'Total Revenue', 'id': 'TotalRevenue'},
                    {'name': 'Operating Income', 'id': 'TotalOperatingIncomeAsReported'},
                    {'name': 'Basic EPS', 'id': 'BasicEPS'},
                    {'name': 'Total Debt', 'id': 'TotalDebt'},
                ],
                style_table={'width': '100%'},
                style_data={'whiteSpace': 'normal', 'height': 'auto'},
                sort_action="native",
                sort_mode="multi",
                filter_action="native",
            )
        ],
    ),
    html.Hr(style={'border': '1px solid lightgray'}),
    html.H2("ChatGPT opinion"),
    # Display ChatGPT message
    html.Div(chatgpt_message, id='chatgpt-opinion-placeholder',
             style={'whiteSpace': 'pre-wrap', 'font-family': 'monospace'}),
    html.Hr(style={'border': '1px solid lightgray'}),
])





# Callback to upload the ISINs
# Callback to upload the ISINs
@app.callback(
    [Output('isin-status', 'children'),
     Output('confirmation-message', 'children')],
    Input('upload-data', 'contents'),
    prevent_initial_call=True
)
def upload_isins(contents):
    if contents is None:
        return "No file uploaded.", None
    
    # Get the content of the uploaded file
    content_type, content_string = contents[0].split(',')
    
    # Construct the file path
    file_path = os.path.join(isin_upload_dir, 'ISIN-Input.csv')
    
    # Process the uploaded ISINs and get the processed count
    processed_count = upload_isins_from_file(file_path, content_string)

    status = f"{processed_count} ISINs could be processed."
    confirmation_message = None

    if processed_count > 0:
        df, profile_df, financials_df = create_data_frames(isin_list)
        save_data_frames(df, profile_df, financials_df)
        confirmation_message = f"DataFrames saved successfully."
    
    return status, confirmation_message







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


@app.callback(
    Output('loading-enhancing', 'children'),
    Input('data-enhancing-button', 'n_clicks'),
    State('isin-status', 'children'),
    prevent_initial_call=True
)
def data_enhancing(n_clicks, isin_status):
    if "could be processed" in isin_status:
        df, profile_df, financials_df = create_data_frames(isin_list)  # Assuming isin_list is accessible
        save_data_frames(df, profile_df, financials_df)
        return None
    else:
        return "Please upload ISINs first."



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
