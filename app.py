import streamlit as st
import pandas as pd
import io

REQUIRED_COLUMNS = ['Date', 'Name', 'Mobile Number']

def extract_required_columns(file, file_type):
    try:
        if file_type == 'csv':
            df = pd.read_csv(file)
        elif file_type == 'xlsx':
            df = pd.read_excel(file)
        else:
            st.warning(f"Unsupported file type: {file.name}")
            return None
        if not all(col in df.columns for col in REQUIRED_COLUMNS):
            st.warning(f"File `{file.name}` skipped. Missing one of the required columns: {REQUIRED_COLUMNS}")
            return None
        return df[REQUIRED_COLUMNS]
    except Exception as e:
        st.error(f"Error reading {file.name}: {e}")
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
    st.title("📂 Merge CSV and Excel Files")
    st.markdown("Upload `.csv` or `.xlsx` files. This tool will extract `Date`, `Name`, and `Mobile Number` columns and let you download the merged result as either a CSV or Excel file.")
    uploaded_files = st.file_uploader(
        "Upload files (CSV or Excel)", 
        type=["csv", "xlsx"],
        accept_multiple_files=True
    )
    if uploaded_files:
        merged_data = []
        for uploaded_file in uploaded_files:
            file_name = uploaded_file.name.lower()
            file_type = 'csv' if file_name.endswith('.csv') else 'xlsx' if file_name.endswith('.xlsx') else None
            extracted_df = extract_required_columns(uploaded_file, file_type)
            if extracted_df is not None:
                merged_data.append(extracted_df)
        if merged_data:
            result_df = pd.concat(merged_data, ignore_index=True)
            st.success("✅ Files processed and merged successfully!")
            # st.dataframe(result_df.head())
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
            st.warning("⚠️ No valid files were processed.")

if __name__ == "__main__":
    main()
