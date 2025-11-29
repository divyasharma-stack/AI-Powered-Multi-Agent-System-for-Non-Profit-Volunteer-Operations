import os
from google import genai
from google.genai.errors import APIError
from sheets_tool import VolunteerSheetTool # Import the tool you just built!

# --- Configuration ---
# TEMPORARY FIX: Hardcoding the API key to bypass environment variable issue.
API_KEY = "YOUR API KEY"

if not API_KEY:
    # This block should now be skipped, but kept for safety.
    print("FATAL ERROR: API Key not found.")
    exit()

# List of required fields for a new volunteer
REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'phone', 'position', 'date_of_joining', 'skills', 'country', 'Availability']


def run_onboarding_agent():
    """Initializes and runs the simple Onboarding Agent conversation."""

    # 1. Initialize the Custom Tool
    sheet_tool = VolunteerSheetTool()
    if not sheet_tool.worksheet:
        print("Agent failed to start: Sheet Tool could not connect.")
        return

    # 2. Initialize the Gemini Client
    try:
        client = genai.Client(api_key=API_KEY)
    except Exception as e:
        print(f"Error initializing Gemini client: {e}")
        return

    # 3. Define the Agent's Role (The System Prompt)
    system_instruction = (
        "You are the friendly 'Onboarding Agent' for a nonprofit organization. "
        "Your goal is to collect specific details from the user (a new volunteer). "
        "You must collect ALL the following details, one by one, and store them in the session: "
        f"{', '.join(REQUIRED_FIELDS)}. "
        "Do not stop until all information is collected. "
        "Start by welcoming the volunteer and asking for their full name."
    )

    # 4. Start the Chat Session (This holds the memory of the conversation)
    # Define the configuration for the model, including the system instruction.
    config = genai.types.GenerateContentConfig(
        system_instruction=system_instruction
    )

    chat_session = client.chats.create(
        model='gemini-2.5-flash',
        config=config # <-- THIS IS THE CORRECT WAY TO PASS THE INSTRUCTION
    )

    print("\n🤖 Onboarding Agent is Live! (Type 'quit' or 'exit' to end the session.)")
    print("-------------------------------------------------------------------")

    volunteer_data = {}

    # The index tracking which question we just finished answering (starts at -1)
    # The loop must run a total of len(REQUIRED_FIELDS) times to capture all data.
    last_answered_index = -1 

    # Loop to simulate a conversation. Runs as long as we haven't answered the last field.
    while last_answered_index < len(REQUIRED_FIELDS) - 1:
        
        # 1. Get user input
        user_input = input("Volunteer: ")
        if user_input.lower() in ['quit', 'exit']:
            print("Session ended by user.")
            return
        
        # 2. Get response from the Gemini model (this usually asks the next question)
        try:
            response = chat_session.send_message(user_input)
            print(f"Agent: {response.text}")
        except APIError as e:
            print(f"API Error: {e}")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break

        # 3. CRITICAL FIX: Extract and Store the Data for the question that was just answered.
        
        last_answered_index += 1
        
        # Special handling for the first name and last name:
        if last_answered_index == 0:
            # We assume the model's first question ("full name") gets parsed into the first two fields
            name_parts = user_input.strip().split()
            if len(name_parts) >= 2:
                volunteer_data['first_name'] = name_parts[0]
                volunteer_data['last_name'] = name_parts[-1]
                last_answered_index += 1 # Advance index by one more to account for 'last_name' being filled
                continue # Skip the rest of the loop and go to the next question
            
            # If only one name was provided, save it as first name only
            volunteer_data['first_name'] = user_input.strip()
            continue # Skip the rest of the loop

        # For all other fields (starting from email, index 2), save the current user_input
        if last_answered_index < len(REQUIRED_FIELDS):
            current_field_to_save = REQUIRED_FIELDS[last_answered_index]
            volunteer_data[current_field_to_save] = user_input.strip()


    # 5. Final Action: Use the Custom Tool to Save Data
    print("\n-------------------------------------------------------------------")
    print("🤖 Agent: Thank you! I have all your details. Processing now...")

    # The dictionary 'volunteer_data' holds the information collected via the chat session's memory.
    final_save_result = sheet_tool.add_new_volunteer(volunteer_data)

    print(f"Agent: Save Result: {final_save_result}")

    if final_save_result.get('status') == 'SUCCESS':
        print("Agent: Onboarding complete! Welcome to the team.")
    else:
        print("Agent: I encountered an error saving your data. Please contact a coordinator.")


if __name__ == "__main__":
    run_onboarding_agent()
