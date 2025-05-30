import streamlit as st
import pandas as pd
import io
import re

REQUIRED_COLUMNS = ['Date', 'Name', 'Mobile Number']

def extract_required_columns(df, source_name):
    if not all(col in df.columns for col in REQUIRED_COLUMNS):
        st.warning(f"`{source_name}` skipped. Missing one of the required columns: {REQUIRED_COLUMNS}")
        return None
    return df[REQUIRED_COLUMNS]

def read_file(file, file_type):
    try:
        if file_type == 'csv':
            df = pd.read_csv(file)
        elif file_type == 'xlsx':
            df = pd.read_excel(file)
        else:
            st.warning(f"Unsupported file type: {file.name}")
            return None
        return extract_required_columns(df, file.name)
    except Exception as e:
        st.error(f"Error reading {file.name}: {e}")
        return None

def fetch_google_sheet_data(url):
    try:
        match = re.search(r'/d/([a-zA-Z0-9-_]+)', url)
        if not match:
            st.warning(f"Invalid Google Sheets URL: {url}")
            return None
        sheet_id = match.group(1)
        export_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        df = pd.read_csv(export_url)
        return extract_required_columns(df, url)
    except Exception as e:
        st.error(f"Error fetching data from Google Sheet: {url}\n. Make sure this sheet could be accessed by \"Anyone with the link\".")
        return None

def generate_csv_file(dataframe):
    output = io.StringIO()
    dataframe.to_csv(output, index=False)
    return output.getvalue()

def generate_excel_file(dataframe):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        dataframe.to_excel(writer, index=False, sheet_name='MergedData')
    output.seek(0)
    return output

def main():
    st.title("📂 Merge CSV, Excel & Google Sheets")
    st.markdown("Upload `.csv`, `.xlsx` files or paste Google Sheets URLs. Then click **Merge Data** to process and download the result.")
    st.markdown("### Upload files manually")
    uploaded_files = st.file_uploader("Upload files (CSV or Excel)", type=["csv", "xlsx"], accept_multiple_files=True)
    if "gsheet_count" not in st.session_state:
        st.session_state.gsheet_count = 1
    st.markdown("### Paste Google Sheets URLs")
    gsheet_urls = []
    for i in range(st.session_state.gsheet_count):
        url = st.text_input(f"Google Sheet URL #{i+1}", key=f"gsheet_url_{i}")
        if url:
            gsheet_urls.append(url)
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("➕ Add another URL"):
            st.session_state.gsheet_count += 1
    merge_clicked = st.button("🔄 Merge Data")
    if merge_clicked:
        merged_data = []
        if uploaded_files:
            for uploaded_file in uploaded_files:
                file_name = uploaded_file.name.lower()
                file_type = 'csv' if file_name.endswith('.csv') else 'xlsx' if file_name.endswith('.xlsx') else None
                extracted_df = read_file(uploaded_file, file_type)
                if extracted_df is not None:
                    merged_data.append(extracted_df)
        for link in gsheet_urls:
            gsheet_df = fetch_google_sheet_data(link)
            if gsheet_df is not None:
                merged_data.append(gsheet_df)
        if merged_data:
            result_df = pd.concat(merged_data, ignore_index=True)
            st.success("✅ Data merged successfully!")
            csv_data = generate_csv_file(result_df)
            excel_data = generate_excel_file(result_df)
            st.download_button(
                label="📥 Download as CSV",
                data=csv_data,
                file_name="merged_output.csv",
                mime="text/csv"
            )
            st.download_button(
                label="📥 Download as Excel (.xlsx)",
                data=excel_data,
                file_name="merged_output.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("⚠️ No valid data found to merge. Please check your files or links.")

if __name__ == "__main__":
    main()
