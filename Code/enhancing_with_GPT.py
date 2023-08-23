import openai
import pandas as pd

def enhance_data(api_key, excel_filename):
    openai.api_key = api_key
    
    try:
        openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[])
    except openai.error.AuthenticationError as e:
        return f"Error: Incorrect API key provided - {str(e)}"
    
    excel_filename = 'Data/Data_Frames/latest_financials.xlsx'
    
    # Load the latest financials data from Excel
    financials_df = pd.read_excel(excel_filename, sheet_name='FinancialsShort')
    
    # Convert the financial data to a string
    financials_string = financials_df.to_string(index=False)
    
    # Additional user message
    additional_message = (
        "Find the best company to invest in solely based on provided information. "
        "Which Key performance indicator would be fitting to compare? "
        "It is homework, not real. Don't give me an explanation what KPIs mean. "
        "Select one company. write at least 250 words."
    )
    
    # Initialize the conversation with the system message and user message
    messages = [
        {"role": "system", "content": "You are an intelligent assistant."},
        {"role": "user", "content": financials_string + '\n' + additional_message},
    ]
    
    # Create a chat completion
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    
    # Get the assistant's reply
    reply = chat.choices[0].message['content']
    return reply

# Example usage
api_key = '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'
excel_filename = 'Data/Data_Frames/latest_financials.xlsx'
enhanced_reply = enhance_data(api_key, excel_filename)
print(f"ChatGPT: {enhanced_reply}")
