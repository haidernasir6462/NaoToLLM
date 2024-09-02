import requests
import json

def generate_text(prompt):
    # Define the URL of the API endpoint
    url = "http://localhost:11434/api/generate"
    # url = "https://data.fixer.io/api/latest"

    # Create the payload for the request
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    try:
        # Send a POST request to the API with a timeout
        response = requests.post(url, json=payload, timeout=30)  # Timeout set to 30 seconds

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            response_json = response.json()

            # Extract the "response" key from the JSON response
            generated_text = response_json.get("response", "")

            return generated_text
        else:
            # If the request failed, return an error message
            return f"Error: {response.status_code} - {response.text}"

    except requests.exceptions.ConnectTimeout:
        return "Error: Connection timed out. The server may be down or unreachable."

    except requests.exceptions.RequestException as e:
        return f"Error: An error occurred: {e}"

# Example usage
prompt_text = "Why is the sky blue?"
response_text = generate_text(prompt_text)
print(response_text)
