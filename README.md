# NaoToLLM

**NaoToLLM** is an open-source project designed to connect Nao robots with Large Language Models (LLMs) such as OpenAI's GPT or Ollama, enabling natural language interactions with the robot. This repository provides the necessary tools and code to facilitate communication between Nao's onboard systems and an external LLM API, allowing Nao to respond intelligently to spoken commands and questions in real time.

## Features

- **Seamless Integration**: Connect Nao robot with various LLMs (e.g., ChatGPT, Ollama) for enhanced conversational capabilities.
- **Real-Time Interaction**: Enable Nao to listen, process, and respond to user inputs via LLMs.
- **Flexible LLM Support**: Easily swap between different LLM APIs with minimal configuration changes.
- **Speech Recognition & Text-to-Speech**: Utilize Nao’s built-in speech recognition and text-to-speech functionalities for smooth communication.
- **Easy Customization**: Modify the interaction flows, conversation logic, and behaviors to suit different applications or LLM use cases.

## Getting Started

### Prerequisites

To run this project, you'll need the following:

- A Nao robot with a working setup.
- Access to an LLM API (e.g., OpenAI API for GPT-3.5/4 or Ollama).
- Python 3.7+ installed on your local machine.
- Naoqi SDK installed for communicating with the Nao robot.

### Installation

1. Clone the repository:
   git clone https://github.com/your-username/NaoToLLM.git
   cd NaoToLLM
   ```
2. Install the required Python dependencies:
   pip install -r requirements.txt
   ``
3. Configure API credentials for the LLM service (e.g., OpenAI API key or Ollama API credentials) 
4. Set up Nao's IP address and port


### Usage

Once everything is set up, you can run the script to enable Nao to communicate with the selected LLM:
Nao will start listening for voice commands, process the input, and send it to the connected LLM. The response will be returned and spoken aloud by the robot.

<!-- ## Project Structure

```plaintext
├── naotollm.py         # Main script to run Nao with LLM integration
├── config.py           # Configuration file for API keys and robot settings
├── llm_interaction.py  # Handles communication with LLM APIs
├── nao_interaction.py  # Manages communication with the Nao robot
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation -->
```

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests. Whether it's improving the code, adding new features, or fixing bugs, we encourage you to get involved.

1. Fork the project.
2. Create your feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## Acknowledgments

- [Naoqi SDK](http://doc.aldebaran.com/) for providing the API to control Nao robots.
- [OpenAI](https://openai.com/) and [Ollama](https://ollama.com/) for their powerful LLM APIs.
