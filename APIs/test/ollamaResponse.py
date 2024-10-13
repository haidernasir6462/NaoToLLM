import requests
import json

# Function to send a request to Ollama API and get the response
def get_ollama_response(user_input):
    conversation_history = []

    # Append the user's input to the conversation history
    conversation_history.append({
        "role": "user",
        "content": user_input + " give just a few lines answer"
    })

    # Define the URL for the Ollama API
    url = 'http://192.168.1.14:11434/api/chat'

    # Prepare the payload with the model and conversation history
    payload = {
        "model": "llama3.1",  # Specify the model name
        "messages": conversation_history
    }

    try:
        # Send POST request to Ollama API
        response = requests.post(url, json=payload)

        # Check if the response status is 200 (OK)
        if response.status_code == 200:
            full_response = ""
            
            # Parse each line of the response
            raw_data = response.text.strip().splitlines()

            for item in raw_data:
                # Load each line as JSON and extract content
                parsed_item = json.loads(item)
                message = parsed_item.get('message', {})
                response_value = message.get('content', "")
                full_response += response_value + " "  # Accumulate the responses

            # Return the accumulated response
            return full_response.strip()

        else:
            return f"Failed to fetch a response. Status code: {response.status_code}"

    except Exception as e:
        # Handle any exceptions
        return f"Exception: {str(e)}"

