Volunteer Ops Agent: AI-Powered Operations
Capstone Project for Kaggle x Google AI Agents Intensive
🎯 Overview
This project develops a modular Multi-Agent System to automate and streamline core administrative tasks for non-profit volunteer operations. The system uses the Gemini API to intelligently process data and generate communications, reducing administrative overhead by automating onboarding, tracking, and reminder processes.
🧠 Architecture
The system is built around three specialized AI agents that share a common data source (Google Sheets) via a custom tool.
Agent
Purpose
Key Functionality
1. Onboarding Agent
Data Capture & Intake
Interactively chats with new volunteers to collect required information (Name, Availability, Skills) and validates/formats the data before writing it to the Volunteer Master Sheet.
2. Tracking Agent
Reporting & Analysis
Runs on demand to analyze the current volunteer pool. It generates a concise status report on total volunteer count, available capacity, and key skill distribution.
3. Reminder Agent
Automation Loop (The "Loop Agent")
Periodically checks the sheet for volunteers with an 'Unresponsive' status. It uses Gemini to draft personalized, professional follow-up messages based on the volunteer's last known activity.

🛠️ Custom Tool Integration
The agents rely on a specialized tool, sheets_tool.py, which handles secure communication with Google Sheets using a Service Account:
VolunteerSheetTool: Provides methods like add_new_volunteer() and get_summary_data() to interact with the master data sheet.
🚀 Getting Started
To run this project, you need a Python environment, a Google Sheet, and API keys.
1. File Structure (Flat)
The project uses a simple, flat structure for ease of deployment:
volunteer-ops-agent/
├── onboarding_agent.py   # Interactive intake agent
├── tracking_agent.py     # Reporting agent
├── reminder_agent.py     # Automation loop agent
├── sheets_tool.py        # Custom Google Sheets integration tool
├── .gitignore            # Excludes keys and environments
└── requirements.txt      # Project dependencies

2. Environment Setup
Install Dependencies: Install all required Python libraries using the requirements.txt file:
pip install -r requirements.txt


Dependencies List:
google-genai
gspread
google-auth


3. API & Credentials
Google Sheet Setup:
Create a new Google Sheet named "Volunteer Master Sheet".
The first row MUST contain these exact headers: first_name, last_name, email, phone, position, date_of_joining, skills, country, Availability. (You may include Status as well if you plan to use it for the Reminder Agent.)
Share the sheet with your Google Service Account email address (Editor access required).
Update the SHEET_ID variable in sheets_tool.py with your sheet's unique ID from the URL.
API Key: Set your Gemini API key as an environment variable before running any agent: export GEMINI_API_KEY="YOUR_API_KEY_HERE" (Mac/Linux) $env:GEMINI_API_KEY="YOUR_API_KEY_HERE" (Windows/PowerShell)
4. Execution Guide
Run the agents from your terminal using the following commands:
Agent
Command
Purpose
Onboarding
python onboarding_agent.py
Starts the interactive chat to collect new volunteer data.
Tracking
python tracking_agent.py
Generates the operational report.
Reminder
python reminder_agent.py
Runs the loop to draft follow-up messages.

📜 License
This project is licensed under the MIT License.

