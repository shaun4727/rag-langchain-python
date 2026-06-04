import os
import requests # 1. Import the requests library
from dotenv import load_dotenv
from langchain.tools import tool
from langchain.agents import create_agent

load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")
if not gemini_key:
    raise ValueError("GEMINI_API_KEY is missing. Check your application environment...")

os.environ["GOOGLE_API_KEY"] = gemini_key

# 2. Modify ONLY the inside of your tool function
@tool
def get_weather(city: str) -> str:
    """Get the current real-time weather for a given city."""
    print(f"🔧 [Tool Execution] Fetching live weather data for: {city}...")
    
    try:
        # Send a network request to a free weather API
        # format=3 returns a clean string like: "San Francisco: ⛅️ +15°C"
        response = requests.get(f"https://wttr.in/{city}?format=3")
        
        # Check if the network call was successful
        response.raise_for_status() 
        
        # Return the actual data back to the LLM
        return response.text 
        
    except requests.RequestException as e:
        # If the API fails or the internet disconnects, tell the LLM gracefully
        return f"Sorry, I could not fetch the weather for {city} right now due to a network error."

# 3. The rest of your agent code remains exactly the same!
agent = create_agent(
    model="google_genai:gemini-2.5-flash-lite",
    tools=[get_weather],
    system_prompt="You are a helpful assistant. Always provide a polite and natural response using the data from your tools.",
)

print("Thinking...")
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in Chandpur Bangladesh right now?"}]}
)

print("\nAgent Response:")
print(result["messages"][-1].content)