# data_frame_utils.py
import pandas as pd
import urllib.request
import json
import yahooquery as yq

def create_data_frames(isin_list):
    import pandas as pd
    import urllib.request
    import json
    import yahooquery as yq
    
    def get_symbol(query, preferred_exchange='AMS'):
        try:
            data = yq.search(query)
        except ValueError: # Will catch JSONDecodeError
            print(query)
        else:
            quotes = data['quotes']
            if len(quotes) == 0:
                return 'No Symbol Found'
    
            symbol = quotes[0]['symbol']
            for quote in quotes:
                if quote['exchange'] == preferred_exchange:
                    symbol = quote['symbol']
                    break
            return symbol
    
    # Read ISINs from CSV file
    isin_df = pd.read_csv('ISIN Input.csv')
    companies = isin_df['ISIN'].tolist()
    
    df = pd.DataFrame({'Company name': companies})
    df['Company symbol'] = df.apply(lambda x: get_symbol(x['Company name']), axis=1)
    
    dataframes = []
    profile_data = []
    financial_data = []  # List to hold financial data
    
    for _, row in df.iterrows():
        company_name = row['Company name']
        company_symbol = row['Company symbol']
        
        url = f"https://query2.finance.yahoo.com/v1/finance/esgChart?symbol={company_symbol}"
        
        connection = urllib.request.urlopen(url)
        data = connection.read()
        data_2 = json.loads(data)
        esg_data = data_2["esgChart"]["result"][0]["symbolSeries"]
        esg_df = pd.DataFrame(esg_data)
        esg_df["timestamp"] = pd.to_datetime(esg_df["timestamp"], unit="s")
        
        # Get long name using Ticker
        ticker = yq.Ticker(company_symbol)
        long_name = ticker.price[company_symbol]['longName']
        
        esg_df['Company name'] = company_name
        esg_df['Company symbol'] = company_symbol
        esg_df['longName'] = long_name
        
        dataframes.append(esg_df)
        
        # Fetch company profile information
        asset_profile = ticker.asset_profile[company_symbol]
        asset_profile['longName'] = long_name
        profile_data.append(asset_profile)
        
        # Fetch financial data using Ticker
        financials = ticker.all_financial_data()
        financials['Company name'] = long_name  # Use longName as company identifier
        financial_data.append(financials)
        
    combined_data = pd.concat(dataframes, ignore_index=True)[[
        'Company name', 'longName', 'Company symbol', 'timestamp', 'esgScore', 
        'governanceScore', 'environmentScore', 'socialScore'
    ]]
    
    # Combine all company profiles into a single DataFrame
    profile_df = pd.DataFrame(profile_data)
    
    # Combine all financial data into a single DataFrame
    financials_df = pd.concat(financial_data, ignore_index=True, keys=df['Company name'])[[
        'Company name', 'asOfDate', 'periodType', 'currencyCode', 'AccountsPayable', 'AccountsReceivable',
        'AccumulatedDepreciation', 'AvailableForSaleSecurities', 'BasicAverageShares', 'BasicEPS',
        'BeginningCashPosition', 'TotalDebt', 'TotalEquityGrossMinorityInterest', 'TotalExpenses',
        'TotalLiabilitiesNetMinorityInterest', 'TotalNonCurrentAssets',
        'TotalNonCurrentLiabilitiesNetMinorityInterest', 'TotalOperatingIncomeAsReported',
        'TotalRevenue', 'TradeandOtherPayablesNonCurrent', 'WorkingCapital'
    ]]
    
    # Create a Pandas Excel writer using ExcelWriter
    excel_filename = 'combined_esg_data.xlsx'
    with pd.ExcelWriter(excel_filename) as writer:
        combined_data.to_excel(writer, sheet_name='ESG Data', index=False)
        profile_df.to_excel(writer, sheet_name='Company Profiles', index=False)
        financials_df.to_excel(writer, sheet_name='Financials', index=True)  # Save financial data to "Financials" sheet
    
    print(f"DataFrames saved to {excel_filename}")
    
    
  
    
    

    return combined_data, profile_df, financials_df

def save_data_frames(df, profile_df, financials_df):
    # Load the combined data Excel file
    excel_filename = 'combined_esg_data.xlsx'
    loaded_excel = pd.read_excel(excel_filename, sheet_name='Financials')
    
    # Group the data by 'Company name' and get the latest row for each company
    latest_financials = loaded_excel.groupby('Company name').apply(lambda group: group[group['asOfDate'] == group['asOfDate'].max()])
    
    # Reset the index and drop the unnecessary level
    latest_financials.reset_index(level=0, drop=True, inplace=True)
    
    # Save the latest financial data to a new Excel file
    output_excel_filename = 'latest_financials.xlsx'
    latest_financials.to_excel(output_excel_filename, sheet_name='FinancialsShort', index=False)
  
    print(f"Latest financial data saved to 'FinancialsShort' sheet in {output_excel_filename}")
