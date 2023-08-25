import os
import openai
import pandas as pd
from tenacity import retry, stop_after_attempt, wait_fixed

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def enhance_data(excel_filename):
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key is None:
        return "Error: OpenAI API key not set"
    
    openai.api_key = api_key
    
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
    assistant_reply = chat.choices[0].message['content']
    
    return assistant_reply

# Example usage
excel_filename = 'Data/Data_Frames/latest_financials.xlsx'
enhanced_reply = enhance_data(excel_filename)
print(f"ChatGPT: {enhanced_reply}")
