import gspread
import os
from typing import Dict, Any

# sheets_tool.py (Lines 6-11 should look like this)
# --- Configuration ---
# Set the path to your service account key file
SERVICE_ACCOUNT_PATH = r"C:\Users\rrajv\..............................."

# Your configuration (already updated in previous steps)
SPREADSHEET_ID = "1dXO8NIfyVEWCdiLx-UbDyoMFgIgB0ucg4t2fYOBF7Jw"
SHEET_NAME = "Sheet1"
# ... rest of the file ...


class VolunteerSheetTool:
    """
    A custom tool for Agents to interact with the Volunteer Google Sheet.
    """
    def __init__(self):
        try:
            # 1. Authenticate using the service account key
            self.gc = gspread.service_account(filename=SERVICE_ACCOUNT_PATH)
            # 2. Open the spreadsheet by its ID
            self.spreadsheet = self.gc.open_by_key(SPREADSHEET_ID)
            # 3. Select the specific worksheet (tab)
            self.worksheet = self.spreadsheet.worksheet(SHEET_NAME)
        except Exception as e:
            print(f"Error connecting to Google Sheets: {e}")
            self.worksheet = None

    def get_all_volunteers(self) -> Dict[str, Any]:
        """
        Reads all data from the Google Sheet and returns it as a dictionary result.
        """
        if not self.worksheet:
            return {'status': 'FAILED', 'error': "Could not connect to the spreadsheet."}

        try:
            # Get all records (rows) as a list of dictionaries
            data = self.worksheet.get_all_records()
            return {'status': 'SUCCESS', 'data': data}
        except Exception as e:
            return {'status': 'FAILED', 'error': f"Error reading data from sheet: {e}"}

    def add_new_volunteer(self, data: dict) -> Dict[str, Any]:
        """
        Adds a new volunteer's data to the Google Sheet.
        Now returns a dictionary for structured error handling.

        Args:
            data: A dictionary containing the volunteer's details.

        Returns:
            A dictionary with 'status' and 'message' or 'error'.
        """
        if not self.worksheet:
            return {'status': 'FAILED', 'error': "Could not connect to the spreadsheet."}

        try:
            # 1. Get the list of column headers from your sheet (Row 1)
            headers = self.worksheet.row_values(1)

            # 2. Create the list of values to append, matching the sheet's column order
            # Note: The data keys must match the header names in your sheet exactly (e.g., 'Availability' vs 'availability')
            row_values = [data.get(header, "") for header in headers]

            # 3. Append the row to the sheet
            self.worksheet.append_row(row_values)

            # 4. Success message (Returns dictionary)
            return {'status': 'SUCCESS', 'message': f"New volunteer {data.get('first_name', 'data')} has been added to the sheet."}

        except Exception as e:
            # Returns a failure dictionary
            return {'status': 'FAILED', 'error': str(e)}


# --- Testing block (Run this file to test your connection) ---
if __name__ == "__main__":
    print("--- Testing Volunteer Sheet Tool ---")

    tool = VolunteerSheetTool()

    # Test 1: Reading data (get_all_volunteers)
    read_result = tool.get_all_volunteers()
    if read_result.get('status') == 'SUCCESS':
        volunteer_data = read_result.get('data', [])
        print(f"\nTest 1 Success: Retrieved {len(volunteer_data)} volunteer records.")
        if len(volunteer_data) > 0:
             print("\nFirst Record Retrieved:")
             print(volunteer_data[0])
    else:
        print(f"\nTest 1 Failed: {read_result.get('error')}")

    # Test 2: Writing data (add_new_volunteer - simulating the Onboarding Agent)
    print("\n--- Testing Writing Data ---")
    new_volunteer_test = {
        'first_name': 'Test',
        'last_name': 'SheetFix', # Updated name to track the successful run
        'email': 'sheet-fix-test@example.com',
        'phone': '0000000000',
        'position': 'Tester',
        'date_of_joining': '2025-11-20',
        'skills': 'Debugging',
        'country': 'USA',
        # NOTE: Keys must match your sheet headers exactly.
        'Availability': '1 hr/week'
    }
    write_result = tool.add_new_volunteer(new_volunteer_test)
    
    # Check the structured result dictionary
    if write_result.get('status') == 'SUCCESS':
        print(f"Test 2 Result: SUCCESS: {write_result.get('message')}")
        print("\nTest 2 Success: Check your Google Sheet! A new row should be added with 'sheet-fix-test@example.com'.")
    else:
        print(f"Test 2 Failed: Error: {write_result.get('error')}")
        print("\nTest 2 Failed: Please check your service_account.json and sheet sharing permissions.")
