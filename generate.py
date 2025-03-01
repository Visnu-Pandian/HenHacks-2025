import os
import json
def generate_ics_and_explanation(client, model, prompt):
    """Generates an .ics file and explanation using Gemini."""

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": {
                "type": "object",
                "properties": {
                    "ics_file": {
                        "type": "string",
                        "description": "The generated .ics file content as a string."
                    },
                    "chain_of_thought": {
                        "type": "string",
                        "description": "A detailed explanation of the scheduling decisions made, including heuristic application and reasoning."
                    }
                },
                "required": ["ics_file", "chain_of_thought"]
            }
        },
    )

    try:
        # Access the response as a dictionary
        response_dict = response.candidates[0].content.parts[0].text
        response_data = json.loads(response_dict) #parse the json string

        ics_content = response_data["ics_file"]
        chain_of_thought = response_data["chain_of_thought"]

        return ics_content, chain_of_thought

    except (AttributeError, IndexError, json.JSONDecodeError, KeyError) as e:
        print(f"Error processing response: {e}")
        print(response) #Print the raw response to help debugging.
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print(response)
        return None, None
    
    

def load_template(file_name):
    TEMPLATES_DIR = "prompt_templates"
    """Load a template from a file."""
    with open(os.path.join(TEMPLATES_DIR, file_name), "r") as file:
        return file.read().strip()

def generate_prompt(**kwargs):
    """Load all templates, merge them, and format dynamically."""
    with open("prompt_templates/prompt_config.json", "r") as config_file:
        config = json.load(config_file)

    # Load templates in the specified order
    prompt_parts = [load_template(file).format(**kwargs) for file in config["order"]]

    # Join sections with a newline
    return "\n\n".join(prompt_parts)