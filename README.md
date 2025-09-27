# Tradebook to Tally Journal Entry Generator

## Overview

This Streamlit app lets you upload an equities/currency/commodity tradebook as a CSV and generates:

- A checklist of ledgers you should create in Tally
- Sample journal entries for each trade (Buy/Sell)
- Simple logic for journal entries (expand for taxes, brokerage, etc.)

## How to Use

1. Prepare your CSV file with the following columns:
   - symbol
   - isin
   - trade_date
   - exchange
   - segment
   - series
   - trade_type
   - auction
   - quantity
   - price
   - order_execution_time

2. Install requirements:
2. Install requirements:
pip install -r requirements.txt


3. Start the app:
streamlit run app.py


4. Open the URL shown by Streamlit, upload your tradebook CSV, and review:
- Required Ledgers
- Sample Journal Entries

5. Use the output to set up ledgers and post entries in Tally. Always review with your accountant!

## Customization

- To handle brokerage, STT, and other charges, expand `app.py` with extra logic.
- For integration with different accounting workflows or formats, modify journal entry generation.

## Disclaimer

This tool is for information and educational purposes only. Always consult a qualified professional before posting accounting entries.

## License

MIT License

Copyright (c) 2025 [Your Name/Organization]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
