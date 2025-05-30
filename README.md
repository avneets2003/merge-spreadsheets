# Merge Spreadsheets App

Upload `.csv` or `.xlsx` files. This tool will extract `Date`, `Name`, and `Mobile Number` columns and let you download the merged result as either a CSV or Excel file.

To run the app locally on your Windows PC, follow the steps below:

- Clone this repository.

- Install Python, if it's not already installed.

- Open PowerShell in the directory where you have cloned this repository.

- Create a virtual environment:

    `python -m venv venv`

- Activate the virtual environment you have just created:

    `./venv/Scripts/activate`

- Upgrade pip, if it's not on the latest version:

    `python -m pip install --upgrade pip`

- Install the required dependencies:

    `pip install -r requirements.txt`

- Run the app:

    `streamlit run app.py`
