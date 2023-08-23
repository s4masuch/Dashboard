# Introduction
This tool is designed for equity researchers to compare user-specified listed companies within a standardized KPI framework. It provides an AI interface with GPT-3.5 for analysis.

# Different Modules
The underlying architecture is modularized.

## Code
- `upload_ISINs.py`: Provides ISIN upload functionality for users. Lists are uploaded to "Data" → "ISIN-Upload". The file is checked to ensure that only valid ISINs are provided and available on Yahoo Finance.
- `create_data_frames.py`: After uploading and validating the ISINs, this module creates data frames containing ESG data, the latest financials, and general company information.
- `enhancing_with_GPT.py`: Creates a merged string based on latest financials and a predefined input in `additional_prompt.py`  

  
# Reliability of Data
[Your content about the reliability of data goes here.]
