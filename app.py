import streamlit as st
import pandas as pd

st.title("Tradebook to Tally Journal Entry Generator")

st.write("""
Upload your tradebook CSV file with these columns:
symbol, isin, trade_date, exchange, segment, series, trade_type, auction, quantity, price, order_execution_time
""")

uploaded_file = st.file_uploader("Upload tradebook CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Standard ledgers for equity trading
    ledgers = set([
        "Broker Account",
        "Trading Account",
        "Demat/Depository Account",
        "Bank Account",
        "Securities Transaction Tax Account",
        "Exchange Charges Account",
        "Profit & Loss A/c",
        "Other Charges Account",
        "GST Account",
    ])
    # Add a separate ledger for each symbol traded
    for symbol in df['symbol'].dropna().unique():
        ledgers.add(f"{symbol} (Trading)")

    st.subheader("Required Ledgers (Create these in Tally):")
    for ledger in sorted(ledgers):
        st.write(f"- {ledger}")

    st.subheader("Sample Accounting Journal Entries:")
    entries = []
    for _, row in df.iterrows():
        symbol = row['symbol']
        qty = row['quantity']
        price = row['price']
        trade_type = str(row['trade_type'])
        date = row['trade_date']
        amount = qty * price
        if trade_type.lower() == "buy":
            entries.append({
                "Date": date,
                "Debit Ledger": f"{symbol} (Trading)",
                "Credit Ledger": "Bank Account",
                "Amount": round(amount, 2),
                "Narration": f"Purchased {qty} shares of {symbol} @ {price}"
            })
        elif trade_type.lower() == "sell":
            entries.append({
                "Date": date,
                "Debit Ledger": "Bank Account",
                "Credit Ledger": f"{symbol} (Trading)",
                "Amount": round(amount, 2),
                "Narration": f"Sold {qty} shares of {symbol} @ {price}"
            })
        # You can expand with additional logic for charges, taxes, etc., if more columns/data available

    entry_df = pd.DataFrame(entries)
    st.dataframe(entry_df.head(20))
    st.info("These journal entries are generated from your uploaded tradebook. Please customize logic for any brokerage, STT or other fees involved as per your business needs.")

st.warning("Disclaimer: This is an automated accounting tool for educational use only. Review all entries with a qualified accountant before posting in Tally.")
