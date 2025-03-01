import os
from dotenv import load_dotenv
from google import genai

# pip install -q -U google-genai
# pip install python-dotenv
load_dotenv()
api_key = os.getenv('API_KEY')

if not api_key:
    raise ValueError("No API key found. Please set the API_KEY environment variable in the .env file.")

client = genai.Client(api_key)

# Example function to use the client
def get_gemini_data(prompt):
    try:
        # Replace 'your_endpoint' with the actual endpoint you want to call
        response = client.get('your_endpoint', params={'prompt': prompt})
        return response.json()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
if __name__ == "__main__":
    prompt = "What is the weather like today?"
    data = get_gemini_data(prompt)
    if data:
        print("Data retrieved successfully:")
        print(data)
    else:
        print("Failed to retrieve data.")