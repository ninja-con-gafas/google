"""
The module provides utilities to interact with Google Sheets using a service account.
"""

from google.oauth2.service_account import Credentials
from gspread import authorize, Spreadsheet
from pandas import DataFrame
from typing import Dict

def get_worksheets(spreadsheet_name: str, credentials: Credentials) -> Dict[str, DataFrame]:

    """
    Retrieves all worksheets from a specified spreadsheet and converts each worksheet into a DataFrame.
    The DataFrame is created using the first row as column headers and the remaining rows as data. The spreadsheet must
    be shared with the service account using its client email.

    args:
        spreadsheet_name (str): The name of the spreadsheet to be accessed.

    returns:
        Dict[str, DataFrame]: A dictionary where the keys are worksheet titles and the values are DataFrames
                              representing the content of each worksheet.

    raises:
        None
    """

    print(f"Loading all the worksheets from the {spreadsheet_name} spreadsheet")
    spreadsheet: Spreadsheet = authorize(credentials).open(spreadsheet_name)
    return {worksheet.title: DataFrame(data=worksheet.get_all_values()[1:],
                                       columns=worksheet.get_all_values()[0])
            for worksheet in spreadsheet.worksheets()}
