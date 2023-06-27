# Importing Packages
from flask import Flask, render_template, request 
import requests
import os
from dotenv import load_dotenv
load_dotenv()

# AI API Setup
hugging_face_token = os.getenv("HUGGING_FACE_TOKEN")
# Model Url -> https://huggingface.co/OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5
API_URL = "https://api-inference.huggingface.co/models/OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5"
headers = {"Authorization": f"Bearer {hugging_face_token}"}
conversations = []

# Initializing app
app = Flask(__name__)

# Home route handler
@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        # Get user input from form
        msg_input = request.form['msg_input']


        # Get chatbot response
        response = get_chatbot_response(prompt=msg_input)

        # Store conversation in conversations list
        conversation = [msg_input, response]
        conversations.append(conversation)

        # Render template with updated conversation
        return render_template('index.html', msg_input=msg_input, conversations=conversations)
    else:
        # Render template initially
        return render_template("index.html")


def query(payload):
    # Send POST request to API
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


def get_chatbot_response(prompt):
    # Get chatbot response from API
    output = query({"inputs": f"<|prompter|>{prompt}<|endoftext|><|assistant|>"})
    print(output[0]['generated_text'])
    return output[0]['generated_text'].split('<|assistant|>')[-1]


if __name__ == "__main__":
    # Run the Flask app in debug mode
    app.run(debug=True)