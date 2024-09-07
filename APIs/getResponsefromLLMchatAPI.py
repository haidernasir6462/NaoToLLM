import requests
import json

# Initialize a global variable to store the conversation history
conversation_history = []

def generate_response(prompt):
    # Define the URL of the API endpoint
    url = "http://192.168.1.12:11434/api/chat"

    # Add the new user message to the conversation history
    conversation_history.append({"role": "user", "content": prompt})

    # Define the payload with the entire conversation history
    payload = {
        "model": "llama3.1",
        "messages": conversation_history  # Send the full conversation history
    }

    try:
        # Send a POST request to the API with a timeout and enable streaming
        response = requests.post(url, json=payload, timeout=30, stream=True)

        # Check if the request was successful
        if response.status_code == 200:
            full_response_text = ""
            
            # Iterate over the response lines
            for line in response.iter_lines():
                if line:  # Check if the line is not empty
                    try:
                        # Parse each line as JSON
                        response_json = json.loads(line.decode('utf-8'))
                        # Extract and concatenate the "content" field from "message"
                        message_content = response_json.get("message", {}).get("content", "")
                        full_response_text += message_content
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {e}")
                        continue

            # Append the assistant's response to the conversation history
            if full_response_text.strip():  # Ensure response is not empty
                conversation_history.append({"role": "assistant", "content": full_response_text})
            
            return full_response_text
        else:
            # If the request failed, return an error message
            return f"Error: {response.status_code} - {response.text}"

    except requests.exceptions.ConnectTimeout:
        return "Error: Connection timed out. The server may be down or unreachable."

    except requests.exceptions.RequestException as e:
        return f"Error: An error occurred: {e}"

# Example usage
response_text = generate_response("Why is the sky blue?")
print(response_text)

# Continue the conversation
response_text = generate_response("What about sunsets?")
print(response_text)
