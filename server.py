from flask import Flask, render_template, request,redirect,url_for
import json

app = Flask(__name__)

user_messages =[]

@app.route('/', methods=['POST','GET'])
@app.route('/home', methods=['POST','GET'])
def home():
    if request.method == "POST":
        msg_input = request.form['msg_input']
        user_messages.append(msg_input)
        return render_template('index.html', msg_input=msg_input,user_messages=user_messages)
        # return json.dumps({'msg_input':msg_input})
    else:
        return render_template("index.html")

@app.route('/chat', methods=['POST','GET'])
def chat(msg):
    msg_input = request.form['msg-input']
    return msg_input

if __name__ == "__main__": 
    app.run(debug=True) 