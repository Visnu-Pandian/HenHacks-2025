import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv('API_KEY')
model = os.getenv('MODEL')

prompt = """List a few popular cookie recipes in JSON format.

Use this JSON schema:

Recipe = {'recipe_name': str, 'ingredients': list[str]}
Return: list[Recipe]"""

client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model=model,
    contents=prompt,
)

# Use the response as a JSON string.
print(response.text)