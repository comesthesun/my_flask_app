from flask import Flask, request, jsonify, render_template
from openai import OpenAI, OpenAIError
import os
from dotenv import load_dotenv
import logging

# Initialize the Flask app
app = Flask(__name__)

# Clear the environment variable
if 'OPENAI_API_KEY' in os.environ:
    del os.environ['OPENAI_API_KEY']

# Load environment variables
load_dotenv()

# Retrieve the OpenAI API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route("/")
def index():
    return render_template("index.html") # Updated to match the provided HTML filename

@app.route('/chat', methods=['POST'])
def chat():
    logging.info('Received request: %s', request.data)
    data = request.get_json()
    user_input = data.get('message')
    conversation = data.get('conversation', [])

    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    # Append the user input to the conversation
    conversation.append({'role': 'user', 'content': user_input})

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=conversation,
            max_tokens=150
        )
        # Get the assistant's response
        assistant_response = response.choices[0].message.content
        conversation.append({'role': 'assistant', 'content': assistant_response})

        result = {'response': assistant_response, 'conversation': conversation}
        logging.info('Response: %s', result)
        return jsonify(result)

    except OpenAIError as e:
        logging.error('OpenAIError: %s', e)
        return jsonify({'error': str(e)}), 501
    except Exception as e:
        logging.error('Unexpected error: %s', e)
        return jsonify({'error': 'An unexpected error occurred'}), 502

# Ensure Flask app runs only when executed directly
if __name__ == '__main__':
    app.run(debug=True, port=8001)
