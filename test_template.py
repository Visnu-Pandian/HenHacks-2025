import os
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()
apiKey = os.getenv('API_KEY')
geminiModel = os.getenv('MODEL')
if not apiKey:
    raise ValueError("API_KEY environment variable not found. Please set it in the .env file.")
if not geminiModel:
    raise ValueError("MODEL environment variable not found. Please set it in the .env file.")

# print(f"API Key: {apiKey}")
# print(f"Model: {geminiModel}")

# Define the prompt
prompt = """List a few popular cookie recipes in JSON format.

Use this JSON schema:

Recipe = {'recipe_name': str, 'ingredients': list[str]}
Return: list[Recipe]"""

client = genai.Client(api_key=apiKey)
# Generate content using the model and prompt
try:
    response = client.models.generate_content(
        model=geminiModel,
        contents=prompt,
    )
    if response and hasattr(response, 'text'):
        # Use the response as a JSON string.
        print(response.text)
    else:
        print("No response or empty response received.")
except Exception as e:
    print(f"An error occurred: {e}")