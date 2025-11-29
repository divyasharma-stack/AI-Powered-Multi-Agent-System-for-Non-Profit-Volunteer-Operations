
import os
from google import genai
from google.genai.errors import APIError
from sheets_tool import VolunteerSheetTool # FLAT STRUCTURE IMPORT

# Uses the environment variable for security, as described in the README
API_KEY = os.environ.get("YOUR API KEY") 

def run_tracking_agent():
    """Initializes and runs the Tracking Agent to generate a volunteer report."""
    
    if not API_KEY:
        print("Error: GEMINI_API_KEY environment variable is not set. Please set it as per README.md.")
        return
        
    # 1. Initialize the Custom Tool
    sheet_tool = VolunteerSheetTool()
    if not sheet_tool.worksheet:
        print("Agent failed to start: Sheet Tool could not connect.")
        return

    # 2. Get Summary Data
    summary_data = sheet_tool.get_summary_data()
    if "error" in summary_data:
        print(f"Error retrieving summary data: {summary_data['error']}")
        return

    # 3. Define the Agent's Role (The System Prompt)
    system_instruction = (
        "You are the 'Volunteer Tracking Agent'. Your task is to analyze raw volunteer metrics "
        "and generate a concise, professional status report for the Operations Coordinator. "
        "The tone should be formal and informative. Do NOT make up any numbers; use only the data provided. "
        "Structure the report with a clear header and bullet points detailing the key metrics."
    )
    
    # 4. Initialize the Gemini Client
    try:
        client = genai.Client(api_key=API_KEY)
    except Exception as e:
        print(f"Error initializing Gemini client: {e}")
        return

    # 5. Create the Prompt with Tool Output
    user_prompt = (
        f"Generate the daily volunteer operations report based on the following raw data: "
        f"{summary_data}"
    )

    print("🤖 Tracking Agent is running...")
    
    # 6. Send Request to Gemini
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[user_prompt],
            config=genai.types.GenerateContentConfig(system_instruction=system_instruction)
        )
        
        print("\n--- Volunteer Operations Report ---")
        print(response.text)
        print("---------------------------------")
        
    except APIError as e:
        print(f"\nAPI Error during report generation: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    run_tracking_agent()
