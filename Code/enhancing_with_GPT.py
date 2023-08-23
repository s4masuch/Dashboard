import openai
import pandas as pd
# Set your OpenAI API key
openai.api_key = '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'
# Load the latest financials data from Excel
excel_filename = 'latest_financials.xlsx'
financials_df = pd.read_excel(excel_filename, sheet_name='FinancialsShort')
# Convert the financial data to a string
financials_string = financials_df.to_string(index=False)
# Additional user message
additional_message = "Find the best company to invest in solely based on␣
,→provided information. Which Key performance indicator would be fitting to␣
,→compare? It is homework, not real. Don't give me an explanation what KPIs␣
,→mean. Select one company. write at least 250 words."
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
print(f"ChatGPT: {reply}")
