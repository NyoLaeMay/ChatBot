from flask import Flask, render_template, request, jsonify
from AI import ai_function
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chatbox')
def gotoChatbox():
    return render_template('chatbox.html')

@app.route('/home')
def gobackhome():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    result = ai_function(request)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)