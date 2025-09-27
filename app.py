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

    # --- Ledger Setup ---
    ledgers = set([
        "Broker Account",
        "Trading Account",
        "Demat/Depository Account",
        "Securities Transaction Tax Account",
        "Exchange Charges Account",
        "Profit & Loss A/c",
        "Other Charges Account",
        "GST Account",
    ])

    for symbol in df['symbol'].dropna().unique():
        ledgers.add(f"{symbol} (Trading)")

    st.subheader("Required Ledgers:")
    for ledger in sorted(ledgers):
        st.write(f"- {ledger}")

    # --- Standard Journal Entry Format ---
    standard_entries = []
    for _, row in df.iterrows():
        symbol = row['symbol']
        qty = row['quantity']
        price = row['price']
        trade_type = str(row['trade_type'])
        date = row['trade_date']
        amount = qty * price
        if trade_type.lower() == "buy":
            standard_entries.append({
                "Date": date,
                "Debit Ledger": f"{symbol} (Trading)",
                "Credit Ledger": "Broker Account",
                "Amount": round(amount, 2),
                "Narration": f"[BUY] Purchased {qty} shares of {symbol} @ {price}; settled with broker"
            })
        elif trade_type.lower() == "sell":
            standard_entries.append({
                "Date": date,
                "Debit Ledger": "Broker Account",
                "Credit Ledger": f"{symbol} (Trading)",
                "Amount": round(amount, 2),
                "Narration": f"[SELL] Sold {qty} shares of {symbol} @ {price}; proceeds from broker"
            })
    standard_df = pd.DataFrame(standard_entries)
    st.subheader("Journal Entries (Standard Format):")
    st.dataframe(standard_df)

    # --- Tally Excel Template Format ---
    tally_entries = []
    voucher_type = "Journal"
    for idx, entry in enumerate(standard_entries):
        # Debit row
        tally_entries.append({
            "Voucher Date": entry['Date'],
            "Voucher Type Name": voucher_type,
            "Voucher Number": idx+1,
            "Voucher Narration": entry['Narration'],
            "Buyer/Supplier - Pincode": "",
            "Ledger Name": entry['Debit Ledger'],
            "Ledger Amount": entry['Amount'],
            "Ledger Amount Dr/Cr": "Dr"
        })
        # Credit row
        tally_entries.append({
            "Voucher Date": entry['Date'],
            "Voucher Type Name": voucher_type,
            "Voucher Number": idx+1,
            "Voucher Narration": entry['Narration'],
            "Buyer/Supplier - Pincode": "",
            "Ledger Name": entry['Credit Ledger'],
            "Ledger Amount": entry['Amount'],
            "Ledger Amount Dr/Cr": "Cr"
        })
    tally_df = pd.DataFrame(tally_entries)
    st.subheader("Journal Entries (Tally Excel Template Format):")
    st.dataframe(tally_df)

    # --- Download Buttons ---
    st.download_button(
        "Download Journal Entries (Standard CSV)",
        standard_df.to_csv(index=False),
        file_name="journal_entries_standard.csv",
        mime="text/csv"
    )
    st.download_button(
        "Download Journal Entries (Tally Template CSV)",
        tally_df.to_csv(index=False),
        file_name="journal_entries_tally_template.csv",
        mime="text/csv"
    )

st.warning("Disclaimer: Automated accounting tool. Review with a qualified accountant before posting in Tally.")
