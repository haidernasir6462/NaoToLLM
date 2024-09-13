import requests
import json

def generate_response(prompt):
    # Define the URL of the API endpoint
    url = "http://192.168.138.153:11434/api/generate"

    # Create the payload for the request
    payload = {
        "model": "llama3.1",
        "prompt": prompt,
        # "stream": False
    }

    try:
        # Send a POST request to the API with a timeout
        response = requests.post(url, json=payload, timeout=30)  # Timeout set to 30 seconds

        # Check if the request was successful
        if response.status_code == 200:
            full_response_text = ""
            
            # Iterate over the response lines
            for line in response.iter_lines():
                if line:  # Check if the line is not empty
                    try:
                        # Parse each line as JSON
                        response_json = json.loads(line.decode('utf-8'))
                        # Extract and concatenate the "response" field
                        full_response_text += response_json.get("response", "")
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {e}")
                        continue

            return full_response_text
        else:
            # If the request failed, return an error message
            return f"Error: {response.status_code} - {response.text}"

    except requests.exceptions.ConnectTimeout:
        return "Error: Connection timed out. The server may be down or unreachable."

    except requests.exceptions.RequestException as e:
        return f"Error: An error occurred: {e}"
