from flask import Flask, request, jsonify, render_template
from openai import OpenAI, OpenAIError
import os
import logging 

app = Flask(__name__)

# Retrieve the OpenAI API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    raise ValueError("No OPENAI_API_KEY provided in environment variables")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route("/")
def index():
    return render_template("chat-render-env-css-0722.html")

@app.route('/chat', methods=['POST'])

def chat():
    logging.info('Received request: %s', request.data)
    data = request.get_json()
    user_input = data.get('message')
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    'role': "user",
                    'content': user_input
                }
            ],
            max_tokens=150
        )
        result = {'response': response.choices[0].message.content}
        logging.info('Response: %s', result)
        return jsonify(result)
    
    except OpenAIError as e:
        logging.error('OpenAIError: %s', e)
        return jsonify({'error': str(e)}), 501

    except Exception as e:
        logging.error('Unexpected error: %s', e)
        return jsonify({'error': 'An unexpected error occurred'}), 502

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))

