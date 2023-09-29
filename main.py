import openai
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"/v1/*": {"origins": "*"}})

openai.api_base = "http://localhost:4891/v1"
#openai.api_base = "https://api.openai.com/v1"
openai.api_key = "not needed for a local LLM"
model = "gg-model-gpt4all-falcon-q4_0"

@app.get("/")
def hello():
    return "Hello Brunei!"

@app.post("/<prompt>")
def query(prompt:str):

    # Make the API request
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=50,
        temperature=0.28,
        top_p=0.95,
        n=1,
        echo=True,
        stream=False
    )

    # Print the generated completion
    print(response)
    return jsonify(response)

@app.post("/v1/query")
@cross_origin()
def formquery():
    print(request.data)
    data = request.get_json()
    if data.get("prompt"):
        prompt = data["prompt"]
    else:
        return jsonify({"error": "No prompt provided"})
    # Make the API request
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=50,
        temperature=0.28,
        top_p=0.95,
        n=1,
        echo=True,
        stream=False
    )

    # Print the generated completion
    response = remove_question_from_response(prompt, response)
    return response

def remove_question_from_response(question, response):
    text = response["choices"][0]["text"]
    return text.replace(question, "")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)