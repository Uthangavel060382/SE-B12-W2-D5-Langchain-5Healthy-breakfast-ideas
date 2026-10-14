
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load API key
load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY is missing")

# Initialize model
llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0.7
)

# Ask the model
response = llm.invoke("Give me 5 healthy breakfast ideas.")

# Print entire response object
print(response)
