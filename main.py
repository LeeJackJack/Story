from flask import Flask, render_template, request, stream_with_context, Response, jsonify
from dotenv import load_dotenv
from generate.text_to_image import generate_and_stream, generate_and_stream_protagonist, generate_and_stream_plot_image
from generate.completions import get_lan_response
from database.models import db, User
import os
from flask_cors import cross_origin
from controllers.user_controller import add_user
from tools.ali_oss import upload_pic
from controllers.protagonist_controller import get_random_protagonist
from controllers.story_plot_controller import get_random_story_plot
from controllers.description_controller import get_description

load_dotenv()  # 加载 .env 文件中的变量
app = Flask(__name__, static_folder='out')

# 使用 os.environ 从 .env 文件中获取配置
DATABASE_USERNAME = os.environ['DATABASE_USERNAME']
DATABASE_PASSWORD = os.environ['DATABASE_PASSWORD']
DATABASE_HOST = os.environ['DATABASE_HOST']
DATABASE_NAME = os.environ['DATABASE_NAME']
DATABASE_URI = f"mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/generateImg', methods=['POST'])
def generate_img():
    prompt = request.json.get('prompt')
    return Response(stream_with_context(generate_and_stream(prompt)), content_type='text/plain')


@app.route('/generateGpt', methods=['GET'])
def generate_gpt():
    response = get_lan_response()
    return jsonify({"response": response})


@app.route('/test', methods=['POST'])
def get_account():
    print('test')


@app.route('/uploadImg', methods=['GET'])
def upload_img():
    return upload_pic('1', '2')


# 测试数据连接
@app.route('/getUser')
def get_user():
    return add_user()


@app.route('/getProtagonist')
def get_protagonist():
    protagonist = get_random_protagonist()
    if protagonist:
        return jsonify(protagonist)
    else:
        return jsonify({"error": "No protagonist found"}), 404


@app.route('/createProtagonistImage', methods=['POST'])
def create_protagonist_image():
    prompt = request.json.get('prompt')
    protagonist_id = request.json.get('protagonist_id')
    return Response(stream_with_context(generate_and_stream_protagonist(prompt, protagonist_id)), content_type='text/plain')


@app.route('/createProtagonist')
def create_protagonist():
    protagonist = get_random_protagonist()
    if protagonist:
        return jsonify(protagonist)
    else:
        return jsonify({"error": "No protagonist found"}), 404


@app.route('/getPlot')
def get_story_plot():
    chapter = request.json.get('chapter')
    theme_id = request.json.get('prompt')
    plot = get_random_story_plot(chapter, theme_id)
    if plot:
        return jsonify(plot)
    else:
        return jsonify({"error": "No protagonist found"}), 404


@app.route('/getPlotImage', methods=['POST'])
def get_story_plot_image():
    # plot_id = request.json.get('plot_id')
    plot_id = 23
    description = get_description(plot_id=plot_id)

    return Response(stream_with_context(generate_and_stream_plot_image(description['content'])), content_type='text/plain')


@app.route('/testAPI', methods=['GET'])
@cross_origin()
def test_api():
    result = get_random_protagonist()
    return jsonify(result)


if __name__ == '__main__':
    app.run()
