# AI Memory Agent

A simple AI Memory Agent built with Python, Streamlit, LangGraph, Gemini 2.5 Flash, SerpApi, and MongoDB.

## Files
- `agent.py` - agent, search tool, and MongoDB functions
- `app.py` - Streamlit UI
- `.env` - API keys and MongoDB URI
- `requirements.txt` - dependencies

## Setup

1. Create a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Add your keys to `.env`:
   ```env
   SERP_API_KEY=your_serpapi_key_here
   GOOGLE_API_KEY=your_google_api_key_here
   MONGODB_URI=your_mongodb_uri_here
   ```
4. Run the app:
   ```bash
   streamlit run app.py
   ```

## Notes
- User messages are saved to MongoDB before the agent runs.
- Assistant responses are saved after the agent responds.
- Chat history is shown in the sidebar and main chat area.
- If a message contains the word `confirm`, a Haan/Nahi radio button appears.