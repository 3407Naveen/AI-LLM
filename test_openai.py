
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OpenAI API key not found!")

client = OpenAI(api_key=api_key)

print("Connecting to OpenAI...")

response = client.responses.create(
    model="gpt-5.5",
    input="Reply with exactly: NOVA AI IS ONLINE"
)

print("SUCCESS!")
print(response.output_text)
