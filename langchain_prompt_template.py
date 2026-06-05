import os
import requests 
from dotenv import load_dotenv
from langchain.tools import tool
from langchain.agents import create_agent

# 1. Import the Prompt Template
from langchain_core.prompts import ChatPromptTemplate 

load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")
if not gemini_key:
    raise ValueError("GEMINI_API_KEY is missing. Check your application environment...")

os.environ["GOOGLE_API_KEY"] = gemini_key

@tool
def get_weather(city: str) -> str:
    """Get the current real-time weather for a given city."""
    print(f"🔧 [Tool Execution] Fetching live weather data for: {city}...")
    
    try:
        response = requests.get(f"https://wttr.in/{city}?format=3")
        response.raise_for_status() 
        return response.text 
        
    except requests.RequestException as e:
        return f"Sorry, I could not fetch the weather for {city} right now due to a network error."

# 2. Setup your Agent (The Engine)
agent = create_agent(
    model="google_genai:gemini-2.5-flash-lite",
    tools=[get_weather],
    system_prompt="You are a helpful assistant. Always provide a polite and natural response using the data from your tools.",
)

# 3. Create your Blueprint (The Template)
# We use placeholders like {location} and {date}
prompt_template = ChatPromptTemplate.from_messages([
    ("human", "What is the weather in {location} right now? Today's date is {date}.")
])

# 4. Inject your dynamic variables into the template
# In a real app, 'location' would come from your Next.js req.json()
formatted_messages = prompt_template.invoke({
    "location": "Chandpur, Bangladesh",
    "date": "Thursday"
})

print("Thinking...")

# 5. Pass the cleanly formatted messages to the agent
result = agent.invoke(
    {"messages": formatted_messages.to_messages()}
)

print("\nAgent Response:")
print(result["messages"][-1].content)