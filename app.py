import streamlit as st
import pandas as pd

st.title("Tradebook to Tally Journal Entry Generator")

st.write("""
Upload your tradebook CSV file with these columns:
symbol, isin, trade_date, exchange, segment, series, trade_type, auction, quantity, price, order_execution_time
""")

uploaded_file = st.file_uploader("Upload tradebook CSV", type="csv")

# Ledger types mapping
ledger_types = {
    "Broker Account": "Sundry Creditor",
    "Trading Account": "Direct Income / Expense",
    "Demat/Depository Account": "Depository",
    "Securities Transaction Tax Account": "Duties & Taxes",
    "Exchange Charges Account": "Indirect Expense",
    "Profit & Loss A/c": "Profit & Loss Account",
    "Other Charges Account": "Indirect Expense",
    "GST Account": "Duties & Taxes",
}

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    ledger_list = []
    for key, ltype in ledger_types.items():
        ledger_list.append({"Ledger Name": key, "Ledger Type": ltype})
    for symbol in df['symbol'].dropna().unique():
        ledger_list.append({
            "Ledger Name": f"{symbol} (Trading)",
            "Ledger Type": "Stock-in-Hand"
        })

    st.subheader("Required Ledgers (Name and Type):")
    ledger_df = pd.DataFrame(ledger_list)
    st.dataframe(ledger_df)

    # --- Journal Entries as before ---
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
    st.download_button(
        "Download Ledgers with Types (CSV)",
        ledger_df.to_csv(index=False),
        file_name="ledger_list_with_types.csv",
        mime="text/csv"
    )

st.info(
    "Disclaimer: This tool is for informational and educational purposes only. "
    "Please consult a qualified accountant or tax advisor before posting entries in Tally. "
    "The accuracy and suitability of these entries should be validated for your specific use case."
)
st.markdown(
    "<div style='text-align:center;font-size:20px;'>Made with ❤️ by Viraj Shah</div>",
    unsafe_allow_html=True
)
