from flask import Flask, request, jsonify, render_template
import openai
import os
from dotenv import load_dotenv
import logging

# Initialize the Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv()

# Retrieve the OpenAI API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')

# Initialize the OpenAI client
openai.api_key = api_key

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route("/")
def index():
    return render_template("chat-render-env-menu.html")

@app.route('/chat', methods=['POST'])
def chat():
    logging.info('Received request: %s', request.data)
    data = request.get_json()
    user_input = data.get('message')
    model = data.get('model', 'gpt-4')
    max_tokens = data.get('max_tokens', 150)
    temperature = data.get('temperature', 0.7)
    conversation = data.get('conversation', [])

    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    # Append the user input to the conversation
    conversation.append({'role': 'user', 'content': user_input})

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=conversation,
            max_tokens=max_tokens,
            temperature=temperature
        )
        # Get the assistant's response
        assistant_response = response.choices[0].message['content']
        conversation.append({'role': 'assistant', 'content': assistant_response})

        result = {'response': assistant_response, 'conversation': conversation}
        logging.info('Response: %s', result)
        return jsonify(result)

    except openai.error.OpenAIError as e:
        logging.error('OpenAIError: %s', e)
        return jsonify({'error': str(e)}), 501
    except Exception as e:
        logging.error('Unexpected error: %s', e)
        return jsonify({'error': 'An unexpected error occurred'}), 502

# Ensure Flask app runs only when executed directly
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
