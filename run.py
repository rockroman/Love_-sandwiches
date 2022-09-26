# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales figures input from the user
    """
    while True:
        print("Please enter the sales data from tehe last Market.")
        print("Data should be six numbers ,separated by commas.")
        print("Example: 10,11,12,14,23,54\n")

        data_str = input('Enter your data here: ') 

        sales_data = data_str.split(",")
       

        if validate_data(sales_data):
            print("Data is valid")
            break

    return sales_data


def validate_data(values):
    """
    Validate users input
    inside try converts all strings values to integers
    raise ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values
    """
    try:
        [int(value) for value in values]       
        if len(values) != 6:
            raise ValueError(
                f"6 values Expected,you provided {len(values)}"
            )
    except ValueError as e:
        print(f"invalid data : {e}, please provide valid data\n")
        return False
    
    return True


def calculate_surplus_data(sales_row):
    """
    Compare sales data with stock data for each
    sandwich type. surplus is equal to sales data minus
    stock data.so positive surplus indicates waste
    while negative extra stock after sale is finished.
    """
    print("Calculating surplus data..\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock.pop()
    stock_row = [int(value) for value in (stock_row)]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = stock - sales
        surplus_data.append(surplus)

    return surplus_data


def update_worksheet(data, worksheet):
    """
    update sheet of data
    passed into this function 
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_updaste = SHEET.worksheet(worksheet)
    worksheet_to_updaste.append_row(data)
    print(f"{worksheet} worksheet updated successfully..\n")


def main():
    """
    run all programm functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")


def get_last_five_entry_sales():
    """
    collect collumns of data from sales worksheet 
    ,collecting the last 5 entries for each sandwich
    and returns the data as a list of lists
    """
    sales = SHEET.worksheet("sales")
   
    columns = []

    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])

    return(columns)
   

    # for col in columns:
    #     last_5=(col[-5:])
             


print("Welcome to love Sandwiches Data Automation..\n")

# main()

sales_columns=get_last_five_entry_sales()