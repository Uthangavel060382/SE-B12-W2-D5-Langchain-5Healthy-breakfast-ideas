
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Step 1: Load environment variables
load_dotenv()

# Step 2: Check OpenAI API key
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY is missing")

# Step 3: Initialize LangChain model
llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)

# Step 4: Define precise prompt
prompt = """
Suggest exactly 5 healthy breakfast ideas.

Requirements:
- Include protein and fiber-rich ingredients.
- Minimize added sugar.
- Give exactly 5 ideas.
- Use a numbered list from 1 to 5.
- Write one idea per line.
- Do not include a title or preamble.
- Do not include explanations or conclusions.
"""

# Step 5: Call the model
response = llm.invoke(prompt)

# Step 6: Print only the response text
print(response.content)
