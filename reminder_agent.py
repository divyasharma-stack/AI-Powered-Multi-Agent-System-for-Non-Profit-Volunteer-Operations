import os
from google import genai
from google.genai.errors import APIError
from sheets_tool import VolunteerSheetTool # FLAT STRUCTURE IMPORT

# Uses the environment variable for security, as described in the README
API_KEY = os.environ.get("YOUR API KEY") 

def run_reminder_agent():
    """
    Initializes and runs the Reminder Agent (Loop Agent).
    It checks the sheet for volunteers needing follow-up and drafts an email.
    """
    if not API_KEY:
        print("Error: GEMINI_API_KEY environment variable is not set. Please set it as per README.md.")
        return

    # 1. Initialize the Custom Tool
    sheet_tool = VolunteerSheetTool()
    if not sheet_tool.worksheet:
        print("Agent failed to start: Sheet Tool could not connect.")
        return

    # 2. Get All Volunteer Data
    all_volunteers = sheet_tool.get_all_volunteers()
    if isinstance(all_volunteers, str):
        print(f"Error retrieving volunteer data: {all_volunteers}")
        return

    # 3. Filter for Unresponsive Volunteers (Simulates the 'Loop' logic)
    unresponsive_volunteers = [
        v for v in all_volunteers if v.get('Status', '').strip().lower() == 'unresponsive'
    ]

    print(f"🤖 Reminder Agent found {len(unresponsive_volunteers)} unresponsive volunteers.")

    if not unresponsive_volunteers:
        print("✅ No follow-up needed today. Exiting.")
        return

    # 4. Process Each Unresponsive Volunteer
    client = genai.Client(api_key=API_KEY)
    
    # Define the agent's persona for drafting emails
    system_instruction = (
        "You are the 'Volunteer Engagement Agent'. Your task is to draft a professional, friendly, "
        "and personalized follow-up email to a volunteer who has gone unresponsive. "
        "The email must be positive, concise, and end with a clear call to action to reply. "
        "The response must be the email content ONLY, starting with 'Subject: [Subject Line]' and using Markdown."
    )

    for i, volunteer in enumerate(unresponsive_volunteers):
        name = volunteer.get('Name', 'Volunteer')
        skill = volunteer.get('Skill', 'unspecified skill')
        
        print(f"\n--- Drafting email for {name} ({i+1}/{len(unresponsive_volunteers)}) ---")
        
        # Create a detailed prompt to guide personalization
        prompt = (
            f"Draft a follow-up email for a volunteer named {name}. "
            f"Their primary skill is listed as {skill}. "
            f"Remind them we need their help and ask if they are still interested."
        )

        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[prompt],
                config=genai.types.GenerateContentConfig(system_instruction=system_instruction)
            )
            
            print(response.text)
            
        except APIError as e:
            print(f"API Error drafting email for {name}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred for {name}: {e}")

if __name__ == "__main__":
    run_reminder_agent()
