# Multi-Agent Incident Response System with LLMs

This project demonstrates a multi-agent system built using LangChain and OpenAI's LLMs to automate incident response.

## Setup

1.  Install dependencies: `pip install -r requirements.txt`
2.  Set your OpenAI API key in a `.env` file: `OPENAI_API_KEY=your-api-key`
3. Configure the system via `configs/config.py`
4. Run the main script: `python main.py`



Create the Folder Structure: Make the directories as shown above.
Create the Files: Copy and paste the code into the corresponding files.
Install Dependencies: Run pip install -r requirements.txt in your terminal (from the project's root directory).
Set API Key: Create a .env file in the root directory and add: OPENAI_API_KEY=your-openai-api-key (replace your-openai-api-key with your actual key).
Run: Execute python main.py from the terminal.
Start FastAPI backend (if not already):

uvicorn api.app:app --reload

Run the Streamlit UI:

streamlit run streamlit_app/ui_app.py
