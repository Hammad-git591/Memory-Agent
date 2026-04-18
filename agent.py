import os
from datetime import datetime
from dotenv import load_dotenv
from serpapi import GoogleSearch
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent
from pymongo import MongoClient

load_dotenv()

# MONGODB SETUP
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["ai_agent"]
collection = db["conversations"]

def save_message(session_id: str, role: str, content: str):
    collection.insert_one({
        "session_id": session_id,
        "role": role,
        "content": content
    })

def get_history(session_id: str):
    messages = collection.find(
        {"session_id": session_id},
        {"_id": 0, "role": 1, "content": 1}
    )
    return [{"role": msg["role"], "content": msg["content"]} for msg in messages]

# SEARCH TOOL
def serpapi_search(query: str):
    """Search the internet using SerpAPI and return top results."""
    params = {
        "q": query,
        "hl": "en",
        "gl": "us",
        "api_key": os.getenv("SERP_API_KEY")
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    if "organic_results" in results:
        return [
            {
                "title": r["title"],
                "link": r["link"],
                "snippet": r.get("snippet", "")
            }
            for r in results["organic_results"][:5]
        ]
    return {"error": "No results found"}

# LLM SETUP
llm = ChatGoogleGenerativeAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    model="gemini-2.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=5
)

# CURRENT DATE
today = datetime.now().strftime("%A, %d %B %Y")

# AGENT SETUP
memory = InMemorySaver()
agent = create_react_agent(
    model=llm,
    tools=[serpapi_search],
    prompt=f"""You are a helpful AI assistant named 'Hammad Agent'.
    You were created by Hammad.
    You are NOT Google, NOT Gemini, NOT ChatGPT.
    If someone asks who made you, say 'I was made by Hammad'.
    If someone asks your name, say 'My name is Hammad Agent'.
    Today's date is {today}. Always use this date when someone asks about today's date or current date.
    """,
    checkpointer=memory
)