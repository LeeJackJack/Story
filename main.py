from flask import Flask, render_template, request, stream_with_context, Response, jsonify
from dotenv import load_dotenv
from generate.text_to_image import generate_and_stream
from generate.completions import get_lan_response

load_dotenv()
app = Flask(__name__, static_folder='out')


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/generateImg', methods=['POST'])
def generate_img():
    prompt = request.json.get('prompt')
    return Response(stream_with_context(generate_and_stream(prompt)), content_type='text/plain')


@app.route('/generateGpt', methods=['POST'])
def generate_gpt():
    prompt = ''
    response = get_lan_response(prompt)
    return jsonify({"response": response})


@app.route('/test', methods=['POST'])
def get_account():
    print('test')


if __name__ == '__main__':
    app.run()
