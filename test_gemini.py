
from dotenv import load_dotenv
from google import genai
import os
import time

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL = "gemini-3.8-flash"

for attempt in range(3):
    try:
        print(f"Attempt {attempt + 1}: Connecting...")

        response = client.models.generate_content(
            model=MODEL,
            contents="Reply with exactly: NOVA AI IS ONLINE"
        )

        print("\nSUCCESS!")
        print(response.text)
        break

    except Exception as error:
        print("\nFAILED:", type(error).__name__)
        print(error)

        if attempt < 2:
            wait = 5 * (2 ** attempt)
            print(f"Retrying in {wait} seconds...")
            time.sleep(wait)
