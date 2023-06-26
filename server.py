from flask import Flask, render_template, request,redirect,url_for
import json
import requests
from dotenv import load_dotenv
import os
load_dotenv()

# AI API Setup
hugging_face_token = os.getenv("HUGGING_FACE_TOKEN")
# API_URL = "https://api-inference.huggingface.co/models/OpenAssistant/falcon-7b-sft-mix-2000"
API_URL = "https://api-inference.huggingface.co/models/OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5"
headers = {"Authorization": f"Bearer {hugging_face_token}"}

app = Flask(__name__)

conversations = []

@app.route('/', methods=['POST','GET'])
@app.route('/home', methods=['POST','GET'])
def home():
    if request.method == "POST":
        msg_input = request.form['msg_input']
        response = get_chatbot_response(prompt=msg_input)
        conversation = [msg_input, response]
        conversations.append(conversation)
        return render_template('index.html', msg_input=msg_input,conversations=conversations)
        # return json.dumps({'msg_input':msg_input})
    else:
        return render_template("index.html")

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def get_chatbot_response(prompt):
    output = query({
        "inputs": f"<|prompter|>{prompt}<|endoftext|><|assistant|>",
    })
    return output[0]['generated_text'].split('<|assistant|>')[-1]


if __name__ == "__main__": 
    app.run(debug=True) 