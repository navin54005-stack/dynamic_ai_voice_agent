🤖 Dynamic Voice Agent
A data-driven Python voice agent that dynamically adapts its identity and responses based on uploaded company datasets. Unlike hardcoded bots, this agent extracts its persona, industry context, and service offerings directly from your business data.

🌟 Key Features
Dynamic Identity Extraction: Automatically parses CSV data to identify company names, representative names, and core services using smart-mapping aliases.

Persistent Learning: Saves conversation patterns to local storage (data/patterns/) to build a knowledge base over time.

Contextual Responses: Generates industry-specific replies by injecting real-time company metadata into its logic.

ML-Ready Architecture: Built-in integration with scikit-learn (TF-IDF and KMeans) for future intent clustering and advanced NLP.

🚀 Getting Started
Prerequisites
Ensure you have Python 3.8+ installed. You will need the following libraries:

Bash

pip install scikit-learn numpy
Installation
Clone the repository:

Bash

git clone https://github.com/@navin54005-stack/dynamic-voice-agent.git
Navigate to the directory:

Bash

cd dynamic-voice-agent
🛠️ Usage
1. Basic Implementation
Initialize the agent and load your business data.

Python

from dynamic_ai_model import DynamicVoiceAgent

# Initialize the agent
agent = DynamicVoiceAgent()

# Example data structure from a CSV
company_data = [{
    "company_name": "TechFlow Solutions",
    "industry": "Software Development",
    "calling_agent_name": "Alex",
    "services": "Cloud Infrastructure"
}]

# Load the data
agent.load_company_data(company_data, columns=list(company_data[0].keys()))
2. Generating Responses
The agent uses the loaded data to personalize its interactions:

Python

response = agent.generate_short_response("What services do you offer?")
print(response) 
# Output: "We offer Cloud Infrastructure for Software Development companies. What interests you most?"
📂 Project Structure
dynamic_ai_model.py: The core logic and DynamicVoiceAgent class.

data/patterns/: Directory where conversation_patterns.json is stored for persistent learning.

📈 Future Roadmap
[ ] Intent Clustering: Implement the KMeans logic to group similar user queries.

[ ] Fuzzy Matching: Integrate thefuzz for more flexible keyword recognition.

[ ] LLM Integration: Use the extracted company profile as a system prompt for OpenAI/Anthropic APIs.

📝 License
Distributed under the MIT License. See LICENSE for more information.
