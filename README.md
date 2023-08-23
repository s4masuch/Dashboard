# Introduction
This tool is designed for equity researchers to compare user-specified listed companies within a standardized KPI framework. It provides an AI interface with GPT-3.5 for analysis.

# Functionalities
The underlying architecture is modularized.

- `upload_ISINs.py`: Provides ISIN upload functionality for users. Lists are uploaded to "Data" → "ISIN-Upload". The file is checked to ensure that only valid ISINs are provided and available on Yahoo Finance.
- `create_data_frames.py`: After uploading and validating the ISINs, this module creates data frames containing ESG data, the latest financials, and general company information.
- `enhancing_with_GPT.py`: Creates a merged string based on latest financials and a predefined input in `additional_prompt.py`
- `create_dashboard.py`: Creates the dashboard based on previously processed modules.

# Reliability of underlying data
Data originates from Yahoo! Finance, established in 1997. It is a vital part of the Yahoo! network, providing financial news, data, and original content. With headquarters in New York City, it offers a wide range of services including stock quotes, financial reports, and personal finance tools. Its 26-year history of reliability has made it a trusted source in the financial world.

Features include comprehensive financial news, cryptocurrency coverage (9,000+ unique coins listed), and online tools for personal finance management. While Yahoo! Finance ranks 20th on SimilarWeb's list of major news websites, it's prudent to cross-reference data from multiple sources for comprehensive research.
